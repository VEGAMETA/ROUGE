from random import choice

from domian.entities.enemy import Enemy
from domian.rules.progression import Level
from domian.templates.enemy import ENEMY_TEMPLATES
from domian.value_objects.enums import EnemyType
from domian.value_objects.position import Position
from domian.value_objects.stats import EnemyStats


class EnemyFactory:
    @staticmethod
    def create_random(position: Position, level: Level = Level.LEVEL_1) -> Enemy:
        return EnemyFactory.create(choice(list(ENEMY_TEMPLATES.keys())), position)

    @staticmethod
    def create(
        enemy_type: EnemyType, position: Position, level: Level = Level.LEVEL_1
    ) -> Enemy:
        template = ENEMY_TEMPLATES[enemy_type]
        health, dexterity, strength = EnemyStats.get(level, template)
        return Enemy(
            type=enemy_type,
            position=position,
            hostility=template.hostility,
            ai=template.ai,
            level=level,
            health=health,
            dexterity=dexterity,
            strength=strength,
        )
