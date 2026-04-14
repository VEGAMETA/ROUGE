from curses import (
    COLOR_BLACK,
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_MAGENTA,
    COLOR_RED,
    COLOR_WHITE,
    COLOR_YELLOW,
)
from dataclasses import dataclass

from domian.value_objects.enums import EnemyType, ItemRarityType, ItemType, TileType


@dataclass
class CursesRenderData:
    character: str = "?"
    color1: int = COLOR_WHITE
    color2: int = COLOR_BLACK


class CursesRenderMap:
    TILE_RENDER_MAP = {
        TileType.UNDEFINED: CursesRenderData("☼"),
        TileType.VOID: CursesRenderData(" "),
        TileType.CORRIDOR: CursesRenderData("▒"),
        TileType.FLOOR: CursesRenderData("·"),  # ░
        TileType.WALL: CursesRenderData("▓"),
        TileType.STAIRS_UP: CursesRenderData("▲"),
        TileType.STAIRS_DOWN: CursesRenderData("▼"),
        TileType.DOOR: CursesRenderData("╫"),  # ╬
    }

    ENEMY_RENDER_MAP = {
        EnemyType.ZOMBIE: CursesRenderData("z", COLOR_GREEN),
        EnemyType.VAMPIRE: CursesRenderData("v", COLOR_RED),
        EnemyType.GHOST: CursesRenderData("g", COLOR_WHITE),
        EnemyType.OGRE: CursesRenderData("o", COLOR_YELLOW),
        EnemyType.SNAKE_MAGE: CursesRenderData("s", COLOR_WHITE),
    }

    ITEM_RENDER_MAP = {
        ItemType.CONSUMABLE: CursesRenderData("c"),
        ItemType.WEAPON: CursesRenderData("w"),
        ItemType.TREASURE: CursesRenderData("t"),
        ItemType.AMULET: CursesRenderData("a"),
        ItemType.UNDEFINED: CursesRenderData("?"),
    }

    RARITY_MAP = {
        ItemRarityType.COMMON: COLOR_WHITE,
        ItemRarityType.RARE: COLOR_BLUE,
        ItemRarityType.EPIC: COLOR_MAGENTA,
        ItemRarityType.LEGENDARY: COLOR_YELLOW,
    }
