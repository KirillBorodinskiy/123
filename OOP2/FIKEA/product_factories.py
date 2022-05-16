from abc import ABC, abstractmethod, ABCMeta
from typing import TypeVar, Generic
from .products import Product, Chair, Table, Bed, Grate, OtherProduct
from .repositories import Repository
from .material_factory import MaterialFactory, MaterialParser
from .material import Material

TProduct = TypeVar('TProduct', bound=Product)  # Říkáme, že TProduct je Product nebo podtřída


class AbstractProductFactory(ABC, Generic[TProduct]):
    @abstractmethod
    def create_product(self, product_properties: dict) -> TProduct:
        pass

    @abstractmethod
    def get_created_type(self) -> type:
        pass

    @abstractmethod
    def get_category_name(self) -> str:
        pass


class ProductFactoryBase(AbstractProductFactory[TProduct], Generic[TProduct], metaclass=ABCMeta):
    def __init__(self,
                 material_repository: Repository[str, Material],
                 material_factory: MaterialFactory,
                 default_discount=0,
                 default_description="Another product!"):
        self.material_repository = material_repository
        self.material_factory = material_factory

        self.default_discount = default_discount
        self.default_description = default_description

    @staticmethod
    def _check_dict_validity(product_properties: dict, *additional_keys: str) -> None:
        if "name" not in product_properties:
            ProductFactoryBase._raise_dict_key_error("Product", "name")
        if "id" not in product_properties:
            ProductFactoryBase._raise_dict_key_error(product_properties["name"], "id")
        if "price" not in product_properties:
            ProductFactoryBase._raise_dict_key_error(product_properties["name"], "price")
        if "material" not in product_properties:
            ProductFactoryBase._raise_dict_key_error(product_properties["name"], "material")

        for k in additional_keys:
            if k not in product_properties:
                ProductFactoryBase._raise_dict_key_error(product_properties["name"], "material")

    @staticmethod
    def _raise_dict_key_error(product_name: str, key_name: str):
        raise KeyError(f"Key {key_name} must be specified for {product_name}")

    def _get_discount_from_product_dict(self, product_properties: dict) -> float:
        return self.default_discount if "discount" not in product_properties \
            else product_properties["discount"]

    def _get_description_from_product_dict(self, product_properties: dict) -> str:
        return self.default_description if "description" not in product_properties \
            else product_properties["description"]

    def _get_material(self, product_properties: dict) -> Material:
        material_type, name, color = MaterialParser.parse_material_string(product_properties["material"])
        material = self.material_repository.get_by_id_or_default(name)
        if material is not None:
            return material

        material = self.material_factory.create_material(material_type, name, color)
        self.material_repository.add_entity(material, name)
        return material


class ChairFactory(ProductFactoryBase[Chair]):
    @staticmethod
    def _check_dict_validity(product_properties: dict, *additional_keys: str) -> None:
        ProductFactoryBase._check_dict_validity(product_properties, "height", "backrest_height", *additional_keys)

    def create_product(self, product_properties: dict) -> Chair:
        self._check_dict_validity(product_properties)
        discount = self._get_discount_from_product_dict(product_properties)
        description = self._get_description_from_product_dict(product_properties)
        material = self._get_material(product_properties)

        # Nyní můžeme vytvořit novou instanci
        return Chair(product_properties["id"],
                     product_properties["name"],
                     product_properties["price"],
                     discount,
                     description,
                     material,
                     product_properties["height"],
                     product_properties["backrest_height"])

    def get_created_type(self) -> type:
        return Chair

    def get_category_name(self) -> str:
        return "Židle"


class TableFactory(ProductFactoryBase[Table]):
    @staticmethod
    def _check_dict_validity(product_properties: dict, *additional_keys: str) -> None:
        ProductFactoryBase._check_dict_validity(product_properties, "height", "width", "depth", *additional_keys)

    def create_product(self, product_properties: dict) -> Table:
        self._check_dict_validity(product_properties)
        discount = self._get_discount_from_product_dict(product_properties)
        description = self._get_description_from_product_dict(product_properties)
        material = self._get_material(product_properties)

        return Table(product_properties["id"],
                     product_properties["name"],
                     product_properties["price"],
                     discount,
                     description,
                     material,
                     product_properties["height"],
                     product_properties["width"],
                     product_properties["depth"])

    def get_created_type(self) -> type:
        return Table

    def get_category_name(self) -> str:
        return "Stoly"


class BedFactory(ProductFactoryBase[Bed]):
    @staticmethod
    def _check_dict_validity(product_properties: dict, *additional_keys: str) -> None:
        ProductFactoryBase._check_dict_validity(product_properties, "height", "width", "depth", *additional_keys)

    def create_product(self, product_properties: dict) -> Bed:
        self._check_dict_validity(product_properties)
        discount = self._get_discount_from_product_dict(product_properties)
        description = self._get_description_from_product_dict(product_properties)
        material = self._get_material(product_properties)

        grate_id = None if "grate_included_id" not in product_properties else product_properties["grate_included_id"]

        return Bed(product_properties["id"],
                   product_properties["name"],
                   product_properties["price"],
                   discount,
                   description,
                   material,
                   product_properties["height"],
                   product_properties["width"],
                   product_properties["depth"],
                   grate_id)

    def get_created_type(self) -> type:
        return Bed

    def get_category_name(self) -> str:
        return "Postele"


class GrateFactory(ProductFactoryBase[Grate]):
    @staticmethod
    def _check_dict_validity(product_properties: dict, *additional_keys: str) -> None:
        ProductFactoryBase._check_dict_validity(product_properties, "width", "depth", *additional_keys)

    def create_product(self, product_properties: dict) -> Grate:
        self._check_dict_validity(product_properties)
        discount = self._get_discount_from_product_dict(product_properties)
        description = self._get_description_from_product_dict(product_properties)
        material = self._get_material(product_properties)

        return Grate(product_properties["id"],
                     product_properties["name"],
                     product_properties["price"],
                     discount,
                     description,
                     material,
                     product_properties["width"],
                     product_properties["depth"])

    def get_created_type(self) -> type:
        return Grate

    def get_category_name(self) -> str:
        return "Rošty"


class OtherProductFactory(ProductFactoryBase[OtherProduct]):
    @staticmethod
    def _check_dict_validity(product_properties: dict, *additional_keys: str) -> None:
        ProductFactoryBase._check_dict_validity(product_properties, *additional_keys)

    def create_product(self, product_properties: dict) -> OtherProduct:
        self._check_dict_validity(product_properties)
        discount = self._get_discount_from_product_dict(product_properties)
        description = self._get_description_from_product_dict(product_properties)
        material = self._get_material(product_properties)

        return OtherProduct(product_properties["id"],
                            product_properties["name"],
                            product_properties["price"],
                            discount,
                            description,
                            material)

    def get_created_type(self) -> type:
        return OtherProduct

    def get_category_name(self) -> str:
        return "Ostatní"
