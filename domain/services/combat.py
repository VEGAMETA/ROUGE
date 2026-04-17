from domain.entities.entity import Character
from domain.entities.game_session import GameSession


class CombatService:
    @staticmethod
    def hit(attacker: Character, defender: Character) -> None:
        defender.health -= attacker.strength + attacker.dexterity * 0.5

    @staticmethod
    def attack(context: GameSession) -> None:
        if context.player_turn:
            defender = context.find_enemy()
            if not defender:
                return
            return CombatService.hit(context.player, defender)
