from dataclasses import dataclass

from infrastructure.vector import Vector2i


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
