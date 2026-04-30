from random import random

from domain.entities.enemy import Enemy
from domain.entities.entity import Character
from domain.entities.game_session import GameSession
from domain.entities.player import Player
from domain.generators.item import ItemFactory
from domain.value_objects.enums import EnemyType, SoundType


class CombatService:
    @staticmethod
    def hit(attacker: Character, defender: Character) -> bool:
        if isinstance(attacker, Player) and isinstance(defender, Enemy):
            if defender.type == EnemyType.VAMPIRE and defender.times_hit == 0:
                defender.times_hit += 1
                return False

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
        context.statistics.attacks_made += 1
        defender = context.find_enemy()
        if not defender:
            return False
        attack = CombatService.hit(context.player, defender)
        context.sounds.put(SoundType.HIT if attack else SoundType.SWING)
        if defender.health <= 0:
            context.statistics.enemies_defeated += 1
            context.points += int(
                defender.level.value * 10
                + defender.strength
                + defender.dexterity
                + defender.max_health
            )
            context.enemies.remove(defender)
            context.sounds.put(SoundType.KILL)
            if random() < 0.4:
                context.items.append(
                    ItemFactory.create_random(defender.position, context.player.level)
                )
            return True
        if attack and isinstance(defender, Enemy) and defender.health > 0:
            if defender.type == EnemyType.OGRE and not defender.resting:
                defender.counter_queued = True
        return True
