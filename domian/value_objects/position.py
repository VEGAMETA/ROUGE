from dataclasses import dataclass

from domian.value_objects.vector import Vector2i


@dataclass
class Size:
    width: int = 0
    height: int = 0


@dataclass
class Position(Vector2i): ...


@dataclass(frozen=True)
class Direction:
    UP = Position(0, -1)
    DOWN = Position(0, 1)
    LEFT = Position(-1, 0)
    RIGHT = Position(1, 0)
    UP_LEFT = Position(-1, -1)
    UP_RIGHT = Position(1, -1)
    DOWN_LEFT = Position(-1, 1)
    DOWN_RIGHT = Position(1, 1)
