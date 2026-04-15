from random import choice

from domain.entities.enemy import Enemy
from domain.rules.progression import Level
from domain.templates.enemy import ENEMY_TEMPLATES
from domain.value_objects.enums import EnemyType
from domain.value_objects.position import Position
from domain.value_objects.stats import EnemyStats


class EnemyFactory:
    @staticmethod
    def create_random(position: Position, level: Level = Level.LEVEL_1) -> Enemy:
        return EnemyFactory.create(choice(list(ENEMY_TEMPLATES.keys())), position)

    @staticmethod
    def create(
        enemy_type: EnemyType, position: Position, level: Level = Level.LEVEL_1
    ) -> Enemy:
        template = ENEMY_TEMPLATES[enemy_type](position=position, level=level)
        health, dexterity, strength = EnemyStats.get(level, template)
        return Enemy(
            position=position,
            health=health,
            max_health=health,
            dexterity=dexterity,
            strength=strength,
            level=level,
            type=enemy_type,
            ai=template.ai,
            hostility=template.hostility,
        )
