from enum import Enum, auto


class ItemType(Enum):
    UNDEFINED = 0
    CONSUMABLE = 1
    WEAPON = 2
    TREASURE = 3
    AMULET = 4


class ConsumableType(Enum):
    UNDEFINED = 0
    HEALTH = 1
    DEXTRISITY = 2
    STRENGTH = 3
    MAX_HEALTH = 4
    MAX_DEXTRISITY = 5
    MAX_STRENGTH = 6


class WeaponType(Enum):
    SWORD = 0
    AXE = 1
    BOW = 2
    STAFF = 3


class Hostility(Enum):
    NEUTRAL = 0
    HOSTILE = 1
    FRIENDLY = 2


class EnemyType(Enum):
    ZOMBIE = auto()
    VAMPIRE = auto()
    GHOST = auto()
    OGRE = auto()
    SNAKE_MAGE = auto()


class NotificationType(Enum):
    DEBUG = -1
    INFO = 0
    WARN = 1
    ERROR = 2
    OK = 3
