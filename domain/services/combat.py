from random import random

from domain.entities.entity import Character
from domain.entities.game_session import GameSession
from domain.entities.player import Player
from domain.generators.item import ItemFactory
from domain.templates.item import ENEMY_DROP
from domain.value_objects.enums import SoundType


class CombatService:
    @staticmethod
    def hit(attacker: Character, defender: Character) -> bool:
        strength = attacker.strength + attacker.dexterity * 0.5
        hitchance = -defender.dexterity
        if isinstance(attacker, Player):
            strength += attacker.weapon.damage if attacker.weapon else 0
            hitchance += attacker.dexterity

        if hitchance < 0:
            if random() <= (-hitchance / 100):
                return False
        defender.health -= strength
        defender.health = max(defender.health, 0)
        return True

    @staticmethod
    def attack(context: GameSession) -> bool:
        defender = context.find_enemy()
        if not defender:
            return False
        attack = CombatService.hit(context.player, defender)
        context.sounds.put(SoundType.HIT if attack else SoundType.SWING)
        if defender.health <= 0:
            context.points += int(
                defender.level * 10
                + defender.strength
                + defender.dexterity
                + defender.max_health
            )
            context.enemies.remove(defender)
            context.sounds.put(SoundType.KILL)
            context.dds += 0.07
            if random() < 0.4:
                context.items.append(
                    ItemFactory.create_random(
                        defender.position, context.player.level, ENEMY_DROP
                    )
                )
        return True
