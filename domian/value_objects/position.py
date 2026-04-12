from dataclasses import dataclass


@dataclass
class Size:
    width: int = 0
    height: int = 0


@dataclass
class Position:
    x: int = 0
    y: int = 0

    def __hash__(self) -> int:
        return hash(hash(self.x) + (self.y))

    def __eq__(self, other: "Position") -> bool:
        return other.x == self.x and other.y == self.y

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, other: "Position") -> "Position":
        return Position(self.x * other.x, self.y * other.y)

    def __truediv__(self, other: "Position") -> "Position":
        return Position(self.x // other.x, self.y // other.y)


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
