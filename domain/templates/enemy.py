from functools import partial

from domain.entities.enemy import Enemy
from domain.value_objects.enums import EnemyType, Hostility

ENEMY_TEMPLATES = {
    EnemyType.ZOMBIE: partial(
        Enemy,
        type=EnemyType.ZOMBIE,
        hostility=Hostility.HOSTILE,
        health=25,
        max_health=25,
        dexterity=3,
        strength=10,
    ),
    EnemyType.VAMPIRE: partial(
        Enemy,
        type=EnemyType.VAMPIRE,
        hostility=Hostility.HOSTILE,
        health=20,
        max_health=20,
        dexterity=15,
        strength=5,
    ),
    EnemyType.GHOST: partial(
        Enemy,
        type=EnemyType.GHOST,
        hostility=Hostility.NEUTRAL,
        health=10,
        max_health=10,
        dexterity=10,
        strength=5,
    ),
    EnemyType.OGRE: partial(
        Enemy,
        type=EnemyType.OGRE,
        hostility=Hostility.HOSTILE,
        health=65,
        max_health=65,
        dexterity=2,
        strength=10,
    ),
    EnemyType.SNAKE_MAGE: partial(
        Enemy,
        type=EnemyType.SNAKE_MAGE,
        hostility=Hostility.HOSTILE,
        health=50,
        max_health=50,
        dexterity=15,
        strength=1,
    ),
}
