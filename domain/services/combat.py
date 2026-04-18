from domain.entities.entity import Character
from domain.entities.game_session import GameSession


class CombatService:
    @staticmethod
    def hit(attacker: Character, defender: Character) -> None:
        defender.health -= attacker.strength + attacker.dexterity * 0.5

    @staticmethod
    def attack(context: GameSession) -> bool:
        defender = context.find_enemy()
        if not defender:
            return False
        CombatService.hit(context.player, defender)
        if defender.health <= 0:
            context.enemies.remove(defender)
            # generate an item on dead enemy position
        return True
