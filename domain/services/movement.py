from domain.entities.entity import Character
from domain.entities.game_session import GameSession
from domain.entities.player import Player
from domain.value_objects.position import Position


class MovementService:
    @staticmethod
    def move(character: Character, new_pos: Position, context: GameSession) -> bool:
        if context.get_obstacle_map()[new_pos.y][new_pos.x]:
            return False
        character.position = new_pos
        if isinstance(character, Player):
            context.statistics.tiles_traversed += 1
        return True
