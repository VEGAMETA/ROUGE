from domain.entities.enemy import Enemy
from domain.rules.progression import (
    ENEMY_HEALTH_FACTOR,
    ENEMY_STATS_FACTOR,
    MAX_LEVEL,
    Level,
)
from domain.value_objects.enums import ItemRarityType
from infrastructure.math import exponent, exponent_saturation, inv_linear, inv_parabola


class ItemRarityWeights:
    @staticmethod
    def get(level: Level) -> dict[ItemRarityType, float]:
        return {
            ItemRarityType.COMMON: inv_linear(level, MAX_LEVEL),
            ItemRarityType.RARE: inv_parabola(level, MAX_LEVEL),
            ItemRarityType.EPIC: exponent_saturation(level, MAX_LEVEL),
            ItemRarityType.LEGENDARY: exponent(level, MAX_LEVEL),
        }


class EnemyStats:
    @staticmethod
    def get(level: Level, enemy: Enemy) -> tuple[int, int, int]:
        health = enemy.health * (1 + ENEMY_HEALTH_FACTOR**level)
        dexterity = enemy.dexterity + ENEMY_STATS_FACTOR * level**0.5
        strength = enemy.strength + ENEMY_STATS_FACTOR * level**0.5
        return (health, dexterity, strength)
