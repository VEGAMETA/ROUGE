from domian.entities.enemy import Enemy
from domian.services.ai import VampireAI, ZombieAI
from domian.value_objects.enums import EnemyType, Hostility

LEVEL_FACTOR = 0.5

ENEMY_TEMPLATES = {
    EnemyType.ZOMBIE: Enemy(
        health=25,
        dexterity=3,
        strength=10,
        hostility=Hostility.HOSTILE,
        ai=ZombieAI(),
    ),
    EnemyType.VAMPIRE: Enemy(
        health=20,
        dexterity=15,
        strength=5,
        hostility=Hostility.HOSTILE,
        ai=VampireAI(),
    ),
    EnemyType.GHOST: Enemy(
        health=10,
        dexterity=10,
        strength=5,
        hostility=Hostility.NEUTRAL,
        ai=None,
    ),
    EnemyType.OGRE: Enemy(
        health=65,
        dexterity=2,
        strength=10,
        hostility=Hostility.HOSTILE,
        ai=None,
    ),
    EnemyType.SNAKE_MAGE: Enemy(
        health=50,
        dexterity=15,
        strength=1,
        hostility=Hostility.HOSTILE,
        ai=None,
    ),
}
