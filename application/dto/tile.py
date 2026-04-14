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
    def to_dto(tile: Tile) -> TileDTO:
        return TileDTO(
            x=tile.position.x,
            y=tile.position.y,
            type=tile.type,
            visible=tile.visible,
            explored=tile.explored,
        )


class TileMapMapper:
    @staticmethod
    def to_dto(tile_map: list[list[Tile]]) -> list[list[TileDTO]]:
        tile_map_dto: list[list[TileDTO]] = []
        for i in range(len(tile_map)):
            tile_map_dto.append([])
            for j in range(len(tile_map[i])):
                tile_map_dto[i].append(TileMapper.to_dto(tile_map[i][j]))
        return tile_map_dto
