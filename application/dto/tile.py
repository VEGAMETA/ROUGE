from dataclasses import dataclass

from domain.entities.tile import Tile
from domain.value_objects.enums import TileType


_PERSISTENT_TYPES: tuple[TileType, ...] = (
    TileType.WALL,
    TileType.DOOR,
    TileType.CORRIDOR,
)


def show_type(tile: Tile) -> TileType:
    if tile.visible:
        return tile.type
    if tile.explored and tile.type in _PERSISTENT_TYPES:
        return tile.type
    return TileType.VOID


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
            show_type=show_type(tile),
            visible=tile.visible,
            explored=tile.explored,
            changed=True,
        )

    @staticmethod
    def refresh(tile: Tile, dto: TileDTO) -> None:
        new_show = show_type(tile)
        if dto.show_type != new_show:
            dto.show_type = new_show
            dto.changed = True
        dto.visible = tile.visible
        dto.explored = tile.explored


class TileMapMapper:
    _cache_id = 0
    _cache: list[list[TileDTO]] = ()

    @staticmethod
    def to_dto(tile_map: list[list[Tile]]) -> list[list[TileDTO]]:
        map_id = id(tile_map)
        if map_id == TileMapMapper._cache_id:
            for row, row_dto in zip(tile_map, TileMapMapper._cache):
                for tile, dto in zip(row, row_dto):
                    TileMapper.refresh(tile, dto)
            return TileMapMapper._cache
        result = [[TileMapper.to_dto(tile) for tile in row] for row in tile_map]
        TileMapMapper._cache = result
        TileMapMapper._cache_id = map_id
        return result
