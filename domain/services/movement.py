from domain.entities.enemy import Enemy
from domain.entities.game_session import GameSession
from domain.entities.tile import OBSTACLES
from domain.value_objects.enums import SoundType
from domain.value_objects.position import Direction, Position


class MovementService:
    @staticmethod
    def move(context: GameSession, direction: Direction) -> None:
        new_position = context.player.position + direction
        if context.tile_map[new_position.y][new_position.x].type in OBSTACLES:
            return
        context.player.position = new_position
        context.player.direction = direction
        context.sounds.append(SoundType.MOVE)

    @staticmethod
    def move_ai(enemy: Enemy, next_position: Position, context: GameSession) -> None:
        # if context.tile_map[next_position.y][next_position.x].type in OBSTACLES:
        #     return
        enemy.position = next_position
