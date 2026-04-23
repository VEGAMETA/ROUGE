from dataclasses import dataclass

from domain.entities.tile import Tile
from domain.value_objects.enums import TileType


@dataclass
class TileDTO:
    x: int
    y: int
    type: TileType
    show_type: TileType
    visible: bool
    explored: bool
    changed: bool


class TileMapper:
    @staticmethod
    def to_dto(tile: Tile) -> TileDTO:
        return TileDTO(
            x=tile.position.x,
            y=tile.position.y,
            type=tile.type,
            show_type=tile.type,
            visible=tile.visible,
            explored=tile.explored,
            changed=True,
        )


class TileMapMapper:
    _cache_id = 0
    _cache: list[list[TileDTO]] = ()

    @staticmethod
    def to_dto(tile_map: list[list[Tile]]) -> list[list[TileDTO]]:
        map_id = id(tile_map)
        if map_id == TileMapMapper._cache_id:
            return TileMapMapper._cache
        result = [[TileMapper.to_dto(tile) for tile in row] for row in tile_map]
        TileMapMapper._cache = result
        TileMapMapper._cache_id = map_id
        return result
