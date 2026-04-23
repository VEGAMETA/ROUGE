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

from domain.value_objects.enums import EnemyType, ItemRarityType, ItemType, TileType


@dataclass
class CursesRenderData:
    character: str = "?"
    color1: int = COLOR_WHITE
    color2: int = COLOR_BLACK


class CursesRenderMap:
    PLAYER_RENDER_DATA = CursesRenderData("\u0040", COLOR_YELLOW)

    TILE_RENDER_MAP = {
        TileType.UNDEFINED: CursesRenderData("\u263c"),  # ?
        TileType.VOID: CursesRenderData("\u0020"),
        TileType.CORRIDOR: CursesRenderData("\u2591"),  # ±
        TileType.FLOOR: CursesRenderData("\u00b7"),  # ú°
        TileType.WALL: CursesRenderData("\u2593"),  # ²
        TileType.STAIRS_UP: CursesRenderData("?"),
        TileType.STAIRS_DOWN: CursesRenderData("?"),
        TileType.DOOR: CursesRenderData("\u2573"),  # ×Î u256b
    }

    ENEMY_RENDER_MAP = {
        EnemyType.ZOMBIE: CursesRenderData("z", COLOR_GREEN),
        EnemyType.VAMPIRE: CursesRenderData("v", COLOR_RED),
        EnemyType.GHOST: CursesRenderData("g", COLOR_BLUE),
        EnemyType.OGRE: CursesRenderData("o", COLOR_MAGENTA),
        EnemyType.SNAKE_MAGE: CursesRenderData("s", COLOR_CYAN),
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
