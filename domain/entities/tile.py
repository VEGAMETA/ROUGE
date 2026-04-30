from dataclasses import dataclass

from domain.entities.entity import Entity2D
from domain.value_objects.enums import TileType

OBSTACLES: tuple[TileType] = (TileType.WALL, TileType.VOID, TileType.UNDEFINED)


@dataclass(eq=False)
class Tile(Entity2D):
    type: TileType
    explored: bool = False
    visible: bool = False
