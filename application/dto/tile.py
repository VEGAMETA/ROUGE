from dataclasses import dataclass

from domian.entities.tile import Tile
from domian.value_objects.enums import TileType


@dataclass
class TileDTO:
    x: int
    y: int
    type: TileType
    visible: bool
    explored: bool


class TileMapper:
    @staticmethod
    def to_dto(tile: Tile):
        return TileDTO(
            x=tile.position.x,
            y=tile.position.y,
            type=tile.type,
            visible=tile.visible,
            explored=tile.explored,
        )
