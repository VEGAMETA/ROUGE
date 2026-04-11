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
class CursesRenderMap:
    character: str = "?"
    color1: int = COLOR_WHITE
    color2: int = COLOR_BLACK


class RenderMap:
    TILE_RENDER_MAP = {
        TileType.VOID: CursesRenderMap(" "),
        TileType.CORRIDOR: CursesRenderMap("•"),
        TileType.FLOOR: CursesRenderMap("░"),
        TileType.WALL: CursesRenderMap("█"),
        TileType.STAIRS_UP: CursesRenderMap("▲"),
        TileType.STAIRS_DOWN: CursesRenderMap("▼"),
        TileType.DOOR: CursesRenderMap("╬"),
    }

    ENEMY_RENDER_MAP = {
        EnemyType.ZOMBIE: CursesRenderMap("z", COLOR_GREEN),
        EnemyType.VAMPIRE: CursesRenderMap("v", COLOR_RED),
        EnemyType.GHOST: CursesRenderMap("g", COLOR_WHITE),
        EnemyType.OGRE: CursesRenderMap("o", COLOR_YELLOW),
        EnemyType.SNAKE_MAGE: CursesRenderMap("s", COLOR_WHITE),
    }

    ITEM_RENDER_MAP = {
        ItemType.CONSUMABLE: CursesRenderMap("c"),
        ItemType.WEAPON: CursesRenderMap("w"),
        ItemType.TREASURE: CursesRenderMap("t"),
        ItemType.AMULET: CursesRenderMap("a"),
        ItemType.UNDEFINED: CursesRenderMap("?"),
    }

    RARITY_MAP = {
        ItemRarityType.COMMON: COLOR_WHITE,
        ItemRarityType.RARE: COLOR_BLUE,
        ItemRarityType.EPIC: COLOR_MAGENTA,
        ItemRarityType.LEGENDARY: COLOR_YELLOW,
    }
