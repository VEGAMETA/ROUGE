from dataclasses import dataclass

from application.dto.enemy import EnemyDTO, EnemyMaper
from application.dto.item import ItemDTO, ItemMapper
from application.dto.player import PlayerDTO, PlayerMapper
from application.dto.tile import TileDTO, TileMapMapper
from domian.entities.game_session import GameSession


@dataclass
class GameStateDTO:
    player: PlayerDTO
    enemies: list[EnemyDTO]
    tile_map: list[list[TileDTO]]
    items: list[ItemDTO]


class GameMapper:
    def to_dto(session: GameSession):
        return GameStateDTO(
            player=PlayerMapper.to_dto(session.player),
            enemies=list(map(EnemyMaper.to_dto, session.enemies)),
            tile_map=TileMapMapper.to_dto(session.tile_map),
            items=list(map(ItemMapper.to_dto, session.items)),
        )
