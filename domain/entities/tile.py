from dataclasses import dataclass

from domain.entities.entity import Entity2D
from domain.value_objects.enums import TileType


@dataclass(eq=False)
class Tile(Entity2D):
    type: TileType
    explored: bool = True
    visible: bool = False
