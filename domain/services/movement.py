from domain.entities.entity import Character
from domain.entities.game_session import GameSession
from domain.value_objects.position import Position


class MovementService:
    @staticmethod
    def move(character: Character, new_pos: Position, context: GameSession) -> bool:
        if context.get_obstacle_map()[new_pos.y][new_pos.x]:
            return False
        character.position = new_pos
        return True
