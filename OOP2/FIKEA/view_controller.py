from dataclasses import dataclass
from typing import Tuple, cast, Dict, Callable, Sequence, Type, TypeVar
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

TFactory = TypeVar("TFactory", )

from .repositories import Repository, DictionaryRepository
from .material import Material
from .material_factory import MaterialFactory
from .products import Product
from .product_factories import AbstractProductFactory, ProductFactoryBase


@dataclass(frozen=True)
class Response:
    status_code: int
    headers: Dict[str, str]
    body: str


material_repository: Repository[str, Material] = DictionaryRepository[str, Material](None, lambda x: x.name)

material_factory: MaterialFactory = MaterialFactory(lambda mat_type, name, color: f"{name} ({color})")

product_repository: Repository[int, Product] = DictionaryRepository[int, Product](None, lambda x: x.id)

factories: Dict[str, AbstractProductFactory] = {}


def register_factory(name: str, factory: Type[ProductFactoryBase]) -> None:
    factories[name] = factory(material_repository, material_factory)

routes: Dict[str, Callable[[Sequence[str]], Response]] = {}


def _initialize_routes(_routes: Dict[str, Callable[[Sequence[str]], Response]]):
    def _route(name: str):
        def deco(func: Callable[[Sequence[str], Sequence[str]], Response]):
            _routes[name] = func
            return func

        return deco

    return _route


route = _initialize_routes(routes)


def _create_product(factory_name, obj):
    new_product = factories[factory_name].create_product(obj)
    product_repository.add_entity(new_product)


def _create_category_products(category_name, object_list):
    if category_name not in factories:
        print(f"Factory for {category_name} not found!")
        return
    print(f"Creating {category_name} products")
    for i in object_list:
        _create_product(category_name, i)


def initialize_repositories():
    # Populace repozitáře z JSONu
    with open("products.json", encoding='utf-8') as f:  # Abychom nemuseli volat f.close() použijeme with satement
        product_dict = json.load(f)

        for k, v in product_dict.items():
            _create_category_products(k, v)


def get_page_menu() -> str:
    return f"""
    <div style="display: flex; flex-direction: row; margin-bottom: 2rem;">
        <div style="margin-left: 1rem;">
            <a href="/">Domů</a>
        </div>
        <div style="margin-left: 1rem;">
            <a href="/products">Všechny produkty</a>
        </div>
        {"".join(list(map(lambda k: f'<div style="margin-left: 1rem;"><a href="/products/{k[0]}">{k[1].get_category_name()}</a></div>',
                          factories.items())))}
    </div>
    """


def get_factories() -> Dict[str, AbstractProductFactory]:
    return factories


def parse_path(request_path: str) -> Tuple[Sequence[str], Sequence[str]]:
    parsed_path = request_path.split("?")
    path, query_args = (parsed_path[0], "") if len(parsed_path) < 2 else (parsed_path[0], parsed_path[1])
    path = path.split("/")
    query_args = query_args.split("&")
    return path[1:], query_args


def not_found(path_args: Sequence[str], query_args: Sequence[str]) -> Response:
    return Response(404,
                    {"Content-type": "text/html; charset=utf-8"},
                    f"""
                <html>
                <head><title>Nenalezeno!</title></head>
                <body>
                {get_page_menu()}
                <p> Stránka nenalezena! </p>
                </body>
                </html>
            """)


def handle_request(handler: BaseHTTPRequestHandler) -> Response:
    # Match
    path, query_args = parse_path(handler.path)
    for index in range(len(path), 0, -1):
        if "/".join(path[:index]) in routes:
            return routes["/".join(path[:index])](path[index:], query_args)
    return not_found(*[*path, *query_args])


def bad_request(path_args: Sequence[str], query_args: Sequence[str]) -> Response:
    return Response(400,
                    {"Content-type": "text/html; charset=utf-8"},
                    f"""
                        <html>
                        <head><title>Špatný požadavek!</title></head>
                        <body>
                        {get_page_menu()}
                        <p> Špatný požadavek! </p>
                        </body>
                        </html>
                        """)
