from dataclasses import dataclass

from application.dto.enemy import EnemyDTO, EnemyMaper
from application.dto.item import ItemDTO, ItemMapper
from application.dto.player import PlayerDTO, PlayerMapper
from application.dto.tile import TileDTO, TileMapper
from domian.entities.game_session import GameSession


@dataclass
class GameStateDTO:
    player: PlayerDTO
    enemies: list[EnemyDTO]
    tiles: list[TileDTO]
    items: list[ItemDTO]


class GameMapper:
    def to_dto(session: GameSession):
        player: PlayerDTO = PlayerMapper.to_dto(session.player)
        enemies: list[EnemyDTO] = list(map(EnemyMaper.to_dto, session.enemies))
        tiles: list[TileDTO] = list(map(TileMapper.to_dto, session.tiles))
        items: list[ItemDTO] = list(map(ItemMapper.to_dto, session.items))

        return GameStateDTO(
            player=player,
            enemies=enemies,
            tiles=tiles,
            items=items,
        )
