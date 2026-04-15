from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generator


@dataclass
class Vector2i:
    x: int = 0
    y: int = 0

    def __hash__(self) -> int:
        return hash(hash(self.x) + (self.y))

    def __eq__(self, other: Vector2i) -> bool:
        return other.x == self.x and other.y == self.y

    def __add__(self, other: Any) -> Vector2i:
        if isinstance(other, Vector2i):
            return type(self)(self.x + other.x, self.y + other.y)
        elif isinstance(other, int):
            return type(self)(self.x + other, self.y + other)
        else:
            return NotImplemented

    def __sub__(self, other: Vector2i) -> Vector2i:
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Vector2i) -> Vector2i:
        return type(self)(self.x * other.x, self.y * other.y)

    def __truediv__(self, other: int) -> Vector2i:
        return type(self)(self.x // other, self.y // other)

    def __iter__(self) -> Generator[int, None, None]:
        yield self.x
        yield self.y
