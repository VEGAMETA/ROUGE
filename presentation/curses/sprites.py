import curses
from dataclasses import dataclass
from enum import IntEnum, auto
from pathlib import Path
from typing import Any, Dict
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
    color_matrix: list[Any | None]


class SpriteService:
    sprites: Dict[SpriteType, Sprite] = {}
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

    @staticmethod
    def nearest_curses_color(r, g, b) -> int:
        best_const = curses.COLOR_WHITE
        best_dist2 = float("inf")
        for const, (pr, pg, pb) in SpriteService.PALETTE:
            dr = r - pr
            dg = g - pg
            db = b - pb
            dist2 = dr * dr + dg * dg + db * db
            if dist2 < best_dist2:
                best_dist2 = dist2
                best_const = const
        return best_const

    @staticmethod
    def png_to_color_matrix(path, alpha_threshold=128, transparent_value=None):
        img = Image.open(path).convert("RGBA")
        w, h = img.size
        px = img.load()

        matrix = [[transparent_value for _ in range(w)] for _ in range(h)]
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if a >= alpha_threshold:
                    matrix[y][x] = SpriteService.nearest_curses_color(r, g, b)
                else:
                    matrix[y][x] = transparent_value
        return matrix, w, h

    @staticmethod
    def sample_sprite_color(sprite_type: SpriteType, u, v, default_color=None):
        if u < 0.0:
            u = 0.0
        if u > 1.0:
            u = 1.0
        if v < 0.0:
            v = 0.0
        if v > 1.0:
            v = 1.0

        sprite = SpriteService.sprites[sprite_type]

        x = min(int(u * sprite.width), sprite.width - 1) if sprite.width > 0 else 0
        y = min(int(v * sprite.height), sprite.height - 1) if sprite.height > 0 else 0

        color = sprite.color_matrix[y][x]
        return default_color if color is None else color

    @classmethod
    def register(cls, sprite: SpriteType, path: Path):
        color_matrix, width, height = SpriteService.png_to_color_matrix(path)
        cls.sprites[sprite] = Sprite(sprite, width, height, color_matrix)


class SpriteAssembler:
    @staticmethod
    def assemble_sprites() -> None:
        SpriteService.register(SpriteType.WALL_1, Path("./static/sprites/wall_1.png"))
        SpriteService.register(SpriteType.WALL_2, Path("./static/sprites/wall_2.png"))
        SpriteService.register(SpriteType.WALL_3, Path("./static/sprites/wall_3.png"))
        SpriteService.register(SpriteType.FLOOR_1, Path("./static/sprites/floor_1.png"))
        SpriteService.register(SpriteType.FLOOR_2, Path("./static/sprites/floor_2.png"))
        SpriteService.register(SpriteType.FLOOR_3, Path("./static/sprites/floor_3.png"))
        SpriteService.register(
            SpriteType.CEILING_1, Path("./static/sprites/ceiling_1.png")
        )
        SpriteService.register(
            SpriteType.CEILING_2, Path("./static/sprites/ceiling_2.png")
        )
        SpriteService.register(
            SpriteType.CEILING_3, Path("./static/sprites/ceiling_3.png")
        )
        SpriteService.register(SpriteType.ZOMBIE, Path("./static/sprites/zombie.png"))
        SpriteService.register(SpriteType.OGRE, Path("./static/sprites/ogre.png"))
        SpriteService.register(SpriteType.VAMPIRE, Path("./static/sprites/vampire.png"))
        SpriteService.register(SpriteType.GHOST, Path("./static/sprites/ghost.png"))
        SpriteService.register(
            SpriteType.SNAKE_MAGE, Path("./static/sprites/snake-mage.png")
        )


class SpriteMap:
    ENEMY_MAP = {
        EnemyType.ZOMBIE: SpriteType.ZOMBIE,
        EnemyType.VAMPIRE: SpriteType.VAMPIRE,
        EnemyType.GHOST: SpriteType.GHOST,
        EnemyType.OGRE: SpriteType.OGRE,
        EnemyType.SNAKE_MAGE: SpriteType.SNAKE_MAGE,
    }
    """THEME_MAP = {
        
    }"""
