from domian.entities.enemy import Enemy
from domian.entities.game_session import GameSession
from domian.entities.player import Player
from domian.value_objects.position import Position, Direction


class MovementService:
    @staticmethod
    def move(entity, session: GameSession, direction: Direction) -> None:
        if isinstance(entity, Player):
            entity.position += direction
            entity.direction = direction
        elif isinstance(entity, Enemy):
            entity.position += entity.ai.next_direction()
