from dataclasses import dataclass
from typing import ClassVar, Union

from .material import Material


@dataclass
class Product:
    id: int
    name: str
    price: float
    discount: float
    description: str
    material: Material

    # Class Var bude anotací datclass ignorován
    # (https://docs.python.org/3/library/dataclasses.html#class-variables)
    # můžeme jej používat jako statické pole pro celou třídu
    total_count_created: ClassVar[int] = 0

    def get_total_price(self) -> float:
        return self.price * (1 - self.discount)

    # Tato metoda se volá po __init__() metodě v dataclasses
    # (https://docs.python.org/3/library/dataclasses.html#post-init-processing)
    def __post_init__(self):
        Product.total_count_created += 1


# Židle
@dataclass
class Chair(Product):
    height: float
    backrest_height: float


# Stoly
@dataclass
class Table(Product):
    height: float
    width: float
    depth: float


# Postele
@dataclass
class Bed(Product):
    height: float
    width: float
    depth: float
    grate_included_id: Union[int, None] = None


# Rošty
@dataclass
class Grate(Product):
    width: float
    depth: float


# Ostatní produkty
@dataclass
class OtherProduct(Product):
    pass