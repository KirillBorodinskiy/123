from typing import Callable
from .material import Material, MaterialType


class MaterialParser:
    @staticmethod  # Statická metoda - lze ji volat na instance i na samotné třídě
    # (není vázaná na data instance)
    def parse_material_string(string_to_parse) -> tuple[MaterialType, str, str]:
        """
        :param string_to_parse: string with following format: Type | Name | Color,
        where Type is one of (case-insensitive) WOOD | METAL | PLASTIC | OTHER
        :return: Tuple[MaterialType, str, str] (MaterialType, Name, Color)
        """
        trimmer: Callable[[str], str] = lambda x: x.strip()
        parse_parts = tuple(map(trimmer, string_to_parse.split("|")))
        if len(parse_parts) != 3:
            raise ValueError(f"Invalid material format string {string_to_parse} - invalid number of args")
        if parse_parts[0].upper() not in MaterialType.__members__:
            raise ValueError(
                f"Invalid material format string {string_to_parse} - {parse_parts[0]} is not a valid material"
            )
        material_type = MaterialType[parse_parts[0].upper()]

        return material_type, parse_parts[1], parse_parts[2]


class MaterialFactory:
    def __init__(self, representative_name_generator: Callable[[MaterialType, str, str], str]):
        self.representative_name_generator = representative_name_generator

    def create_material(self, material_type, material_name, color, representative_name = None) -> Material:
        return Material(material_type,
                        material_name,
                        color,
                        representative_name if representative_name
                        else self.representative_name_generator(material_type, material_name, color))

    def create_material_from_string(self, string_to_parse: str):
        material_type, name, color = MaterialParser.parse_material_string(string_to_parse)
        return Material(material_type,
                        name,
                        color,
                        self.representative_name_generator(material_type, name, color))
