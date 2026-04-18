from dataclasses import dataclass

from application.dto.enemy import EnemyDTO, EnemyMaper
from application.dto.item import ItemDTO, ItemMapper
from application.dto.player import PlayerDTO, PlayerMapper
from application.dto.tile import TileDTO, TileMapMapper
from domain.entities.game_session import GameSession


@dataclass
class GameStateDTO:
    player: PlayerDTO
    enemies: list[EnemyDTO]
    tile_map: list[list[TileDTO]]
    items: list[ItemDTO]


class GameMapper:
    def to_dto(context: GameSession):
        return GameStateDTO(
            player=PlayerMapper.to_dto(context.player),
            enemies=list(map(EnemyMaper.to_dto, context.enemies)),
            tile_map=TileMapMapper.to_dto(context.tile_map),
            items=list(map(ItemMapper.to_dto, context.items)),
        )
