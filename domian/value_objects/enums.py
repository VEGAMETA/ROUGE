from enum import IntEnum, auto


class Level(IntEnum):
    LEVEL_1: int = 0
    LEVEL_2: int = 1
    LEVEL_3: int = 2
    LEVEL_4: int = 3
    LEVEL_5: int = 4
    LEVEL_6: int = 5
    LEVEL_7: int = 6
    LEVEL_8: int = 7
    LEVEL_9: int = 8


class NotificationType(IntEnum):
    DEBUG: int = auto()
    INFO: int = auto()
    WARN: int = auto()
    ERROR: int = auto()
    OK: int = auto()


class TileType(IntEnum):
    VOID: int = auto()
    FLOOR: int = auto()
    CORRIDOR: int = auto()
    WALL: int = auto()
    DOOR: int = auto()
    STAIRS_UP: int = auto()
    STAIRS_DOWN: int = auto()


class ItemType(IntEnum):
    UNDEFINED: int = auto()
    CONSUMABLE: int = auto()
    WEAPON: int = auto()
    TREASURE: int = auto()
    AMULET: int = auto()


class ConsumableType(IntEnum):
    UNDEFINED: int = auto()
    HEALTH: int = auto()
    DEXTRISITY: int = auto()
    STRENGTH: int = auto()
    MAX_HEALTH: int = auto()
    MAX_DEXTRISITY: int = auto()
    MAX_STRENGTH: int = auto()


class WeaponType(IntEnum):
    SWORD: int = auto()
    AXE: int = auto()
    BOW: int = auto()
    STAFF: int = auto()


class Hostility(IntEnum):
    NEUTRAL: int = auto()
    HOSTILE: int = auto()
    FRIENDLY: int = auto()


class EnemyType(IntEnum):
    ZOMBIE: int = auto()
    VAMPIRE: int = auto()
    GHOST: int = auto()
    OGRE: int = auto()
    SNAKE_MAGE: int = auto()


class ItemRarityType(IntEnum):
    COMMON: int = auto()
    RARE: int = auto()
    EPIC: int = auto()
    LEGENDARY: int = auto()
