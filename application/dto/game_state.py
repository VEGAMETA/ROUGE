from dataclasses import dataclass

from application.dto.door import DoorDTO, DoorMapper
from application.dto.enemy import EnemyDTO, EnemyMaper
from application.dto.item import ItemDTO, ItemMapper
from application.dto.key import KeyDTO, KeyMapper
from application.dto.player import PlayerDTO, PlayerMapper
from application.dto.tile import TileDTO, TileMapMapper
from domain.entities.game_session import GameSession


@dataclass
class GameStateDTO:
    player: PlayerDTO
    enemies: list[EnemyDTO]
    tile_map: list[list[TileDTO]]
    items: list[ItemDTO]
    doors: list[DoorDTO]
    keys: list[KeyDTO]


class GameMapper:
    def to_dto(context: GameSession):
        return GameStateDTO(
            player=PlayerMapper.to_dto(context.player),
            enemies=[EnemyMaper.to_dto(enemy) for enemy in context.enemies],
            tile_map=TileMapMapper.to_dto(context.tile_map),
            items=[ItemMapper.to_dto(item) for item in context.items],
            doors=[DoorMapper.to_dto(door) for door in context.doors],
            keys=[KeyMapper.to_dto(key) for key in context.keys],
        )
