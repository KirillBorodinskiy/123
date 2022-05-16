from dataclasses import dataclass
from enum import Enum

class MaterialType(Enum):
    WOOD = 1
    METAL = 2
    PLASTIC = 3
    OTHER = 4

@dataclass
class Material:
    material_type: MaterialType
    color: str
    name: str
    representative_name: str

    def __str__(self):
        return self.representative_name
