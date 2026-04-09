from copy import deepcopy
from random import choice

from domian.entities.enemy import Enemy
from domian.templates.enemy import ENEMY_TEMPLATES, LEVEL_FACTOR
from domian.value_objects.enums import EnemyType
from domian.value_objects.position import Position


class EnemyFactory:
    @staticmethod
    def create_random(position: Position) -> Enemy:
        return EnemyFactory.create(choice(list(ENEMY_TEMPLATES.keys())), position)

    @staticmethod
    def create(enemy_type: EnemyType, position: Position, level: int = 0) -> Enemy:
        template = ENEMY_TEMPLATES[enemy_type]
        enemy = deepcopy(template)
        enemy.position = position
        enemy.level = template.level
        enemy.health, enemy.dexterity, enemy.strength = map(
            lambda x: int(x * (1 + enemy.level * LEVEL_FACTOR)),
            (template.health, template.dexterity, template.strength),
        )
        return enemy
