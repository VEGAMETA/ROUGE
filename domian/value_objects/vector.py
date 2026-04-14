from dataclasses import dataclass
from typing import overload


@dataclass
class Vector2i:
    x: int = 0
    y: int = 0

    def __hash__(self) -> int:
        return hash(hash(self.x) + (self.y))

    def __eq__(self, other: "Vector2i") -> bool:
        return other.x == self.x and other.y == self.y

    def __add__(self, other: "Vector2i") -> "Vector2i":
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2i") -> "Vector2i":
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other: "Vector2i") -> "Vector2i":
        return type(self)(self.x * other.x, self.y * other.y)

    def __truediv__(self, other: int) -> "Vector2i":
        return type(self)(self.x // other, self.y // other)
