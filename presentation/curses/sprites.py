import curses
from dataclasses import dataclass
from enum import IntEnum, auto
from pathlib import Path
from typing import Optional

from PIL import Image

from domain.value_objects.enums import (
    DoorType,
    EnemyType,
    ItemType,
    KeyType,
    StairsType,
)


class SpriteType(IntEnum):
    UNDEFINED: int = auto()
    WALL: int = auto()
    FLOOR: int = auto()
    CEILING: int = auto()
    WALL_1: int = auto()
    WALL_2: int = auto()
    WALL_3: int = auto()
    FLOOR_1: int = auto()
    FLOOR_2: int = auto()
    FLOOR_3: int = auto()
    CEILING_1: int = auto()
    CEILING_2: int = auto()
    CEILING_3: int = auto()
    ZOMBIE: int = auto()
    VAMPIRE: int = auto()
    GHOST: int = auto()
    OGRE: int = auto()
    SNAKE_MAGE: int = auto()
    MIMIC1: int = auto()
    MIMIC2: int = auto()
    TREASURE: int = auto()
    CONSUMABLES: int = auto()
    WEAPONS: int = auto()
    SCROLL: int = auto()
    DOOR_OPENED: int = auto()
    DOOR_RED: int = auto()
    DOOR_GREEN: int = auto()
    DOOR_BLUE: int = auto()
    KEY_RED: int = auto()
    KEY_GREEN: int = auto()
    KEY_BLUE: int = auto()
    STAIRCASE: int = auto()


class ThemeType(IntEnum):
    UNDEFINED: int = auto()
    THEME_1: int = auto()
    THEME_2: int = auto()
    THEME_3: int = auto()


@dataclass
class Sprite:
    type: SpriteType
    color_matrix: list[Optional[int]]
    width: int
    height: int


class SpriteMap:
    PALETTE: dict[int, tuple[int, int, int]] = {
        curses.COLOR_BLACK: (0, 0, 0),
        curses.COLOR_RED: (255, 0, 0),
        curses.COLOR_GREEN: (0, 255, 0),
        curses.COLOR_YELLOW: (255, 255, 0),
        curses.COLOR_BLUE: (0, 0, 255),
        curses.COLOR_MAGENTA: (255, 0, 255),
        curses.COLOR_CYAN: (0, 255, 255),
        curses.COLOR_WHITE: (255, 255, 255),
    }

    ENEMY_MAP: dict[EnemyType, SpriteType] = {
        EnemyType.UNDEFINED: SpriteType.UNDEFINED,
        EnemyType.ZOMBIE: SpriteType.ZOMBIE,
        EnemyType.VAMPIRE: SpriteType.VAMPIRE,
        EnemyType.GHOST: SpriteType.GHOST,
        EnemyType.OGRE: SpriteType.OGRE,
        EnemyType.SNAKE_MAGE: SpriteType.SNAKE_MAGE,
    }
    ITEM_MAP: dict[EnemyType, SpriteType] = {
        ItemType.UNDEFINED: SpriteType.UNDEFINED,
        ItemType.CONSUMABLE: SpriteType.CONSUMABLES,
        ItemType.WEAPON: SpriteType.WEAPONS,
        ItemType.TREASURE: SpriteType.TREASURE,
        ItemType.SCROLL: SpriteType.SCROLL,
    }

    DOOR_MAP: dict[DoorType, SpriteType] = {
        DoorType.RED: SpriteType.DOOR_RED,
        DoorType.GREEN: SpriteType.DOOR_GREEN,
        DoorType.BLUE: SpriteType.DOOR_BLUE,
        DoorType.OPENED: SpriteType.DOOR_OPENED,
    }

    KEY_MAP: dict[KeyType, SpriteType] = {
        KeyType.RED: SpriteType.KEY_RED,
        KeyType.GREEN: SpriteType.KEY_GREEN,
        KeyType.BLUE: SpriteType.KEY_BLUE,
    }

    STAIRS_MAP: dict[int, SpriteType] = {
        StairsType.UNDEFINED: SpriteType.STAIRCASE,
        StairsType.UP: SpriteType.STAIRCASE,
        StairsType.DOWN: SpriteType.STAIRCASE,
    }

    SPRITE_PATHS: dict[SpriteType, Path] = {
        SpriteType.UNDEFINED: Path("./static/sprites/error.png"),
        SpriteType.WALL_1: Path("./static/sprites/interior/wall_1.png"),
        SpriteType.WALL_2: Path("./static/sprites/interior/wall_2.png"),
        SpriteType.WALL_3: Path("./static/sprites/interior/wall_3.png"),
        SpriteType.FLOOR_1: Path("./static/sprites/interior/floor_1.png"),
        SpriteType.FLOOR_2: Path("./static/sprites/interior/floor_2.png"),
        SpriteType.FLOOR_3: Path("./static/sprites/interior/floor_3.png"),
        SpriteType.CEILING_1: Path("./static/sprites/interior/ceiling_1.png"),
        SpriteType.CEILING_2: Path("./static/sprites/interior/ceiling_2.png"),
        SpriteType.CEILING_3: Path("./static/sprites/interior/ceiling_3.png"),
        SpriteType.ZOMBIE: Path("./static/sprites/enemies/zombie.png"),
        SpriteType.OGRE: Path("./static/sprites/enemies/ogre.png"),
        SpriteType.VAMPIRE: Path("./static/sprites/enemies/vampire.png"),
        SpriteType.GHOST: Path("./static/sprites/enemies/ghost.png"),
        SpriteType.SNAKE_MAGE: Path("./static/sprites/enemies/snake-mage.png"),
        SpriteType.MIMIC1: Path("./static/sprites/enemies/mimic1.png"),
        SpriteType.MIMIC2: Path("./static/sprites/enemies/mimic2.png"),
        SpriteType.TREASURE: Path("./static/sprites/items/treasure.png"),
        SpriteType.CONSUMABLES: Path("./static/sprites/items/consumables.png"),
        SpriteType.WEAPONS: Path("./static/sprites/items/weapons.png"),
        SpriteType.SCROLL: Path("./static/sprites/items/scroll.png"),
        SpriteType.DOOR_OPENED: Path("./static/sprites/interior/door_opened.png"),
        SpriteType.DOOR_RED: Path("./static/sprites/interior/door_red.png"),
        SpriteType.DOOR_GREEN: Path("./static/sprites/interior/door_green.png"),
        SpriteType.DOOR_BLUE: Path("./static/sprites/interior/door_blue.png"),
        SpriteType.KEY_RED: Path("./static/sprites/items/key_red.png"),
        SpriteType.KEY_GREEN: Path("./static/sprites/items/key_green.png"),
        SpriteType.KEY_BLUE: Path("./static/sprites/items/key_blue.png"),
        SpriteType.STAIRCASE: Path("./static/sprites/staircase.png"),
    }

    THEME_MAP: dict[ThemeType, dict[SpriteType, SpriteType]] = {
        ThemeType.THEME_1: {
            SpriteType.WALL: SpriteType.WALL_1,
            SpriteType.FLOOR: SpriteType.FLOOR_1,
            SpriteType.CEILING: SpriteType.CEILING_1,
        },
        ThemeType.THEME_2: {
            SpriteType.WALL: SpriteType.WALL_2,
            SpriteType.FLOOR: SpriteType.FLOOR_2,
            SpriteType.CEILING: SpriteType.CEILING_2,
        },
        ThemeType.THEME_3: {
            SpriteType.WALL: SpriteType.WALL_3,
            SpriteType.FLOOR: SpriteType.FLOOR_3,
            SpriteType.CEILING: SpriteType.CEILING_3,
        },
    }


class Sprites:
    def __init__(self) -> None:
        self.sprites: dict[SpriteType, Sprite] = {}
        for sprite, path in SpriteMap.SPRITE_PATHS.items():
            self.sprites[sprite] = Sprite(sprite, *self.png_to_color_matrix(path))

    def nearest_curses_color(self, r: float, g: float, b: float) -> int:
        best_const: int = curses.COLOR_WHITE
        best_dist2: float = float("inf")
        for const, (pr, pg, pb) in SpriteMap.PALETTE.items():
            dr: float = r - pr
            dg: float = g - pg
            db: float = b - pb
            dist2: float = dr * dr + dg * dg + db * db
            if dist2 < best_dist2:
                best_dist2 = dist2
                best_const = const
        return best_const

    def png_to_color_matrix(
        self,
        path: Path,
        alpha_threshold: int = 128,
        transparent_value: Optional[int] = None,
    ) -> tuple[list[Optional[int]], int, int]:
        img: Image.Image = Image.open(path).convert("RGBA")
        w: int
        h: int
        r: float
        g: float
        b: float
        a: float
        w, h = img.size
        px: Image.core.PixelAccess = img.load()
        matrix: list[list[Optional[int]]] = [[transparent_value] * w for _ in range(h)]
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                matrix[y][x] = (
                    transparent_value
                    if a < alpha_threshold
                    else self.nearest_curses_color(r, g, b)
                )
        return matrix, w, h

    def sample_sprite_color(
        self,
        sprite_type: SpriteType,
        u: float,
        v: float,
        default_color: int = None,
        theme: Optional[ThemeType] = None,
    ) -> Optional[int]:
        if theme:
            theme_type: Optional[dict[SpriteType, SpriteType]] = (
                SpriteMap.THEME_MAP.get(theme)
            )
            if theme_type is None:
                return default_color
            theme_sprite_type: Optional[SpriteType] = theme_type.get(sprite_type)
            if theme_sprite_type is None:
                return default_color
            sprite_type = theme_sprite_type[sprite_type]
        u = min(1, max(0, u))
        v = min(1, max(0, v))
        sprite: Sprite = self.sprites.get(sprite_type)
        if sprite is None:
            return default_color
        x: int = min(int(u * sprite.width), sprite.width - 1)
        y: int = min(int(v * sprite.height), sprite.height - 1)
        color: Optional[int] = sprite.color_matrix[y][x]
        return default_color if color is None else color


SpriteService = Sprites()
