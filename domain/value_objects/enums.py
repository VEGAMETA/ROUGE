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
    SCROLL: int = auto()


class TreasureType(IntEnum):
    UNDEFINED: int = auto()
    SILVER: int = auto()
    GOLD: int = auto()
    GEM: int = auto()
    RUBY: int = auto()
    SAPPHIRE: int = auto()


class ConsumableType(IntEnum):
    UNDEFINED: int = auto()
    HEALTH: int = auto()
    MAX_HEALTH: int = auto()
    DEXTERITY: int = auto()
    STRENGTH: int = auto()
    FOOD: int = auto()


class WeaponType(IntEnum):
    UNDEFINED: int = auto()
    DAGGER: int = auto()
    MACE: int = auto()
    SWORD: int = auto()
    SPEAR: int = auto()
    AXE: int = auto()
    STAFF: int = auto()
    TWO_HANDED_SWORD: int = auto()


class EnemyType(IntEnum):
    UNDEFINED: int = auto()
    ZOMBIE: int = auto()
    VAMPIRE: int = auto()
    GHOST: int = auto()
    OGRE: int = auto()
    SNAKE_MAGE: int = auto()
    MIMIC1: int = auto()
    MIMIC2: int = auto()


class EnemyAction(IntEnum):
    UNDEFINED: int = auto()
    MOVE: int = auto()
    ATTACK: int = auto()
    FLEE: int = auto()


class ItemRarityType(IntEnum):
    COMMON: int = 0
    RARE: int = 2
    EPIC: int = 5
    LEGENDARY: int = 10


class DoorType(IntEnum):
    RED: int = auto()
    GREEN: int = auto()
    BLUE: int = auto()
    OPENED: int = auto()


class KeyType(IntEnum):
    RED: int = auto()
    GREEN: int = auto()
    BLUE: int = auto()


class StairsType(IntEnum):
    UNDEFINED: int = auto()
    UP: int = auto()
    DOWN: int = auto()


class SoundType(IntEnum):
    STOP: int = auto()
    MUSIC: int = auto()
    UI: int = auto()
    MOVE: int = auto()
    SWING: int = auto()
    HIT: int = auto()
    DEATH: int = auto()
    ITEM_PICK: int = auto()
    ITEM_USE: int = auto()
    KILL: int = auto()
    LEVEL_UP: int = auto()
    DOOR: int = auto()


class Theme3D(IntEnum):
    THEME_1: int = auto()
    THEME_2: int = auto()
    THEME_3: int = auto()
