from dataclasses import dataclass

from domian.value_objects.enums import TileType
from domian.value_objects.position import Position


@dataclass
class Tile:
    type: TileType
    position: Position
    explored: bool = True
    visible: bool = False
