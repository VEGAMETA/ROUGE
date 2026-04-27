from curses import (
    COLOR_BLACK,
    COLOR_BLUE,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_MAGENTA,
    COLOR_RED,
    COLOR_WHITE,
    COLOR_YELLOW,
)
from dataclasses import dataclass

from domain.value_objects.enums import (
    DoorType,
    EnemyType,
    ItemRarityType,
    ItemType,
    KeyType,
    TileType,
)


@dataclass
class CursesRenderData:
    character: str = "?"
    color1: int = COLOR_WHITE
    color2: int = COLOR_BLACK


class CursesRenderMap:
    PLAYER_RENDER_DATA = CursesRenderData("\u0040", COLOR_YELLOW)
    STAIRS_RENDER_DATA = CursesRenderData("\u25bc")

    TILE_RENDER_MAP = {
        TileType.UNDEFINED: CursesRenderData("\u263c"),  # \u263c
        TileType.VOID: CursesRenderData("\u0020"),
        TileType.CORRIDOR: CursesRenderData("\u2591"),
        TileType.FLOOR: CursesRenderData("\u00b7"),
        TileType.WALL: CursesRenderData("\u2593"),
        TileType.DOOR: CursesRenderData("\u2573"),
    }

    ENEMY_RENDER_MAP = {
        EnemyType.UNDEFINED: CursesRenderData("?"),
        EnemyType.ZOMBIE: CursesRenderData("z", COLOR_GREEN),
        EnemyType.VAMPIRE: CursesRenderData("v", COLOR_RED),
        EnemyType.GHOST: CursesRenderData("g", COLOR_BLUE),
        EnemyType.OGRE: CursesRenderData("o", COLOR_MAGENTA),
        EnemyType.SNAKE_MAGE: CursesRenderData("s", COLOR_CYAN),
        EnemyType.MIMIC1: CursesRenderData("ŧ", COLOR_WHITE),
        EnemyType.MIMIC2: CursesRenderData("m", COLOR_YELLOW),
    }

    ITEM_RENDER_MAP = {
        ItemType.UNDEFINED: CursesRenderData("?"),
        ItemType.CONSUMABLE: CursesRenderData("c"),
        ItemType.WEAPON: CursesRenderData("w"),
        ItemType.TREASURE: CursesRenderData("t"),
        ItemType.SCROLL: CursesRenderData("s", COLOR_CYAN),
    }

    KEY_RENDER_MAP = {
        KeyType.UNDEFINED: CursesRenderData("k", COLOR_WHITE),
        KeyType.RED: CursesRenderData("k", COLOR_RED),
        KeyType.GREEN: CursesRenderData("k", COLOR_GREEN),
        KeyType.BLUE: CursesRenderData("k", COLOR_BLUE),
    }

    _door_char = TILE_RENDER_MAP[TileType.DOOR].character

    DOOR_RENDER_MAP = {
        DoorType.UNDEFINED: CursesRenderData(_door_char, COLOR_WHITE),
        DoorType.RED: CursesRenderData(_door_char, COLOR_RED),
        DoorType.GREEN: CursesRenderData(_door_char, COLOR_GREEN),
        DoorType.BLUE: CursesRenderData(_door_char, COLOR_BLUE),
    }

    RARITY_MAP = {
        ItemRarityType.COMMON: COLOR_BLACK,
        ItemRarityType.RARE: COLOR_BLUE,
        ItemRarityType.EPIC: COLOR_MAGENTA,
        ItemRarityType.LEGENDARY: COLOR_YELLOW,
    }
