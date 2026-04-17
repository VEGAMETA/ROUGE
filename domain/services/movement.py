from typing import Optional

from domain.entities.game_session import GameSession
from domain.value_objects.enums import SoundType, TileType
from domain.value_objects.position import Direction


class MovementService:
    @staticmethod
    def move(session: GameSession, direction: Optional[Direction] = None) -> None:
        if direction:
            new_position = session.player.position + direction
            if session.tile_map[new_position.y][new_position.x].type not in (
                TileType.FLOOR,
                TileType.DOOR,
                TileType.CORRIDOR,
            ):
                return
            session.player.position = new_position
            session.player.direction = direction
            session.sounds.append(SoundType.MOVE)
            return
        for enemy in session.enemies:
            enemy.position += enemy.ai.next_direction(session)
