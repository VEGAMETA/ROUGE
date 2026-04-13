from enum import IntEnum, auto


class DefaultRotation(IntEnum):
    SOUTH: int = 0
    EAST: int = 90
    NORTH: int = 180
    WEST: int = 270


class DoorSide(IntEnum):
    UNDEFINED: int = auto()
    TOP: int = auto()
    BOTTOM: int = auto()
    LEFT: int = auto()
    RIGHT: int = auto()


class TileType(IntEnum):
    UNDEFINED: int = auto()
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
    UNDEFINED: int = auto()
    SWORD: int = auto()
    AXE: int = auto()
    BOW: int = auto()
    STAFF: int = auto()


class Hostility(IntEnum):
    UNDEFINED: int = auto()
    NEUTRAL: int = auto()
    HOSTILE: int = auto()
    FRIENDLY: int = auto()


class EnemyType(IntEnum):
    UNDEFINED: int = auto()
    ZOMBIE: int = auto()
    VAMPIRE: int = auto()
    GHOST: int = auto()
    OGRE: int = auto()
    SNAKE_MAGE: int = auto()


class ItemRarityType(IntEnum):
    UNDEFINED: int = auto()
    COMMON: int = auto()
    RARE: int = auto()
    EPIC: int = auto()
    LEGENDARY: int = auto()
