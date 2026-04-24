import curses
from dataclasses import dataclass
from enum import IntEnum, auto
from pathlib import Path

from PIL import Image

from domain.value_objects.enums import EnemyType


class SpriteType(IntEnum):
    UNDEFINED: int = auto()
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


@dataclass(eq=False)
class Sprite:
    type: SpriteType
    width: int
    height: int
    color_matrix: list[int | None]


class SpriteMap:
    ENEMY_MAP = {
        EnemyType.ZOMBIE: SpriteType.ZOMBIE,
        EnemyType.VAMPIRE: SpriteType.VAMPIRE,
        EnemyType.GHOST: SpriteType.GHOST,
        EnemyType.OGRE: SpriteType.OGRE,
        EnemyType.SNAKE_MAGE: SpriteType.SNAKE_MAGE,
    }

    SPRITE_PATHS: dict[SpriteType, Path] = {
        SpriteType.WALL_1: Path("./static/sprites/wall_1.png"),
        SpriteType.WALL_2: Path("./static/sprites/wall_2.png"),
        SpriteType.WALL_3: Path("./static/sprites/wall_3.png"),
        SpriteType.FLOOR_1: Path("./static/sprites/floor_1.png"),
        SpriteType.FLOOR_2: Path("./static/sprites/floor_2.png"),
        SpriteType.FLOOR_3: Path("./static/sprites/floor_3.png"),
        SpriteType.CEILING_1: Path("./static/sprites/ceiling_1.png"),
        SpriteType.CEILING_2: Path("./static/sprites/ceiling_2.png"),
        SpriteType.CEILING_3: Path("./static/sprites/ceiling_3.png"),
        SpriteType.ZOMBIE: Path("./static/sprites/zombie.png"),
        SpriteType.OGRE: Path("./static/sprites/ogre.png"),
        SpriteType.VAMPIRE: Path("./static/sprites/vampire.png"),
        SpriteType.GHOST: Path("./static/sprites/ghost.png"),
        SpriteType.SNAKE_MAGE: Path("./static/sprites/snake-mage.png"),
    }

    """THEME_MAP = {
        
    }"""


class Sprites:
    sprites: dict[SpriteType, Sprite] = {}
    PALETTE = [
        (curses.COLOR_BLACK, (0, 0, 0)),
        (curses.COLOR_RED, (255, 0, 0)),
        (curses.COLOR_GREEN, (0, 255, 0)),
        (curses.COLOR_YELLOW, (255, 255, 0)),
        (curses.COLOR_BLUE, (0, 0, 255)),
        (curses.COLOR_MAGENTA, (255, 0, 255)),
        (curses.COLOR_CYAN, (0, 255, 255)),
        (curses.COLOR_WHITE, (255, 255, 255)),
    ]

    def __init__(self):
        for sprite, path in SpriteMap.SPRITE_PATHS.items():
            color_matrix, width, height = self.png_to_color_matrix(path)
            self.sprites[sprite] = Sprite(sprite, width, height, color_matrix)

    def nearest_curses_color(self, r, g, b) -> int:
        best_const = curses.COLOR_WHITE
        best_dist2 = float("inf")
        for const, (pr, pg, pb) in self.PALETTE:
            dr = r - pr
            dg = g - pg
            db = b - pb
            dist2 = dr * dr + dg * dg + db * db
            if dist2 < best_dist2:
                best_dist2 = dist2
                best_const = const
        return best_const

    def png_to_color_matrix(self, path, alpha_threshold=128, transparent_value=None):
        img = Image.open(path).convert("RGBA")
        w, h = img.size
        px = img.load()
        matrix = [[transparent_value] * w for _ in range(h)]
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                matrix[y][x] = (
                    transparent_value
                    if a < alpha_threshold
                    else self.nearest_curses_color(r, g, b)
                )
        return matrix, w, h

    def sample_sprite_color(self, sprite_type: SpriteType, u, v, default_color=None):
        u = min(1, max(0, u))
        v = min(1, max(0, v))
        sprite = self.sprites[sprite_type]
        x = min(int(u * sprite.width), sprite.width - 1)
        y = min(int(v * sprite.height), sprite.height - 1)
        color = sprite.color_matrix[y][x]
        return default_color if color is None else color


SpriteService = Sprites()
