from functools import partial

from domain.entities.enemy import Enemy
from domain.value_objects.enums import EnemyType

ENEMY_TEMPLATES = {
    EnemyType.ZOMBIE: partial(
        Enemy,
        type=EnemyType.ZOMBIE,
        hostility=7,
        health=30,
        max_health=30,
        dexterity=3,
        strength=7,
    ),
    EnemyType.VAMPIRE: partial(
        Enemy,
        type=EnemyType.VAMPIRE,
        hostility=10,
        health=30,
        max_health=30,
        dexterity=10,
        strength=7,
    ),
    EnemyType.GHOST: partial(
        Enemy,
        type=EnemyType.GHOST,
        hostility=5,
        health=10,
        max_health=10,
        dexterity=10,
        strength=3,
    ),
    EnemyType.OGRE: partial(
        Enemy,
        type=EnemyType.OGRE,
        hostility=7,
        health=40,
        max_health=40,
        dexterity=3,
        strength=15,
    ),
    EnemyType.SNAKE_MAGE: partial(
        Enemy,
        type=EnemyType.SNAKE_MAGE,
        hostility=10,
        health=40,
        max_health=40,
        dexterity=15,
        strength=1,
    ),
}
