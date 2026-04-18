from __future__ import annotations

from dataclasses import dataclass

from infrastructure.vector import Vector2i


@dataclass
class Position(Vector2i):
    def is_adjacent(self, other: Position) -> bool:
        if abs(self.x - other.x) > 1 or abs(self.y - other.y) > 1:
            return False
        return True


@dataclass(frozen=True)
class Direction:
    UNDEFINED = Position()
    UP = Position(0, -1)
    DOWN = Position(0, 1)
    LEFT = Position(-1, 0)
    RIGHT = Position(1, 0)
    UP_LEFT = Position(-1, -1)
    UP_RIGHT = Position(1, -1)
    DOWN_LEFT = Position(-1, 1)
    DOWN_RIGHT = Position(1, 1)
