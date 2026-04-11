from domian.entities.enemy import Enemy
from domian.services.ai import VampireAI, ZombieAI
from domian.value_objects.enums import EnemyType, Hostility

ENEMY_TEMPLATES = {
    EnemyType.ZOMBIE: Enemy(
        type=EnemyType.ZOMBIE,
        hostility=Hostility.HOSTILE,
        ai=ZombieAI(),
        health=25,
        dexterity=3,
        strength=10,
    ),
    EnemyType.VAMPIRE: Enemy(
        type=EnemyType.VAMPIRE,
        hostility=Hostility.HOSTILE,
        ai=VampireAI(),
        health=20,
        dexterity=15,
        strength=5,
    ),
    EnemyType.GHOST: Enemy(
        type=EnemyType.GHOST,
        hostility=Hostility.NEUTRAL,
        ai=None,
        health=10,
        dexterity=10,
        strength=5,
    ),
    EnemyType.OGRE: Enemy(
        type=EnemyType.OGRE,
        hostility=Hostility.HOSTILE,
        ai=None,
        health=65,
        dexterity=2,
        strength=10,
    ),
    EnemyType.SNAKE_MAGE: Enemy(
        type=EnemyType.SNAKE_MAGE,
        hostility=Hostility.HOSTILE,
        ai=None,
        health=50,
        dexterity=15,
        strength=1,
    ),
}
