from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generator


@dataclass
class Vector2:
    x: float = 0
    y: float = 0

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: Vector2) -> bool:
        return other.x == self.x and other.y == self.y

    def __add__(self, other: Any) -> Vector2:
        if isinstance(other, type(self)):
            return type(self)(self.x + other.x, self.y + other.y)
        elif isinstance(other, int):
            return type(self)(self.x + other, self.y + other)
        elif isinstance(other, float):
            return type(self)(self.x + other, self.y + other)
        else:
            return NotImplemented

    def __sub__(self, other: Vector2) -> Vector2:
        if isinstance(other, type(self)):
            return type(self)(self.x - other.x, self.y - other.y)
        elif isinstance(other, int):
            return type(self)(self.x - other, self.y - other)
        elif isinstance(other, float):
            return type(self)(self.x - other, self.y - other)
        else:
            return NotImplemented

    def __mul__(self, other: Any) -> Vector2:
        if isinstance(other, type(self)):
            return type(self)(self.x * other.x, self.y * other.y)
        elif isinstance(other, int):
            return type(self)(self.x * other, self.y * other)
        elif isinstance(other, float):
            return type(self)(self.x * other, self.y * other)
        else:
            return NotImplemented

    def __div__(self, other: Any) -> Vector2:
        if isinstance(other, type(self)):
            return type(self)(self.x / other.x, self.y / other.y)
        elif isinstance(other, int):
            return type(self)(self.x / other, self.y / other)
        elif isinstance(other, float):
            return type(self)(self.x / other, self.y / other)
        else:
            return NotImplemented

    def __truediv__(self, other: int) -> Vector2:
        return type(self)(self.x // other, self.y // other)

    def __iter__(self) -> Generator[int, None, None]:
        yield self.x
        yield self.y

    def length(self) -> float:
        return (self.x * self.x + self.y * self.y) ** 0.5


@dataclass
class Vector2i(Vector2):
    x: int = 0
    y: int = 0

    def __init__(self, x=0, y=0) -> None:
        super().__init__(x, y)
        self.x = int(x)
        self.y = int(y)

    def __add__(self, other: Any) -> Vector2i:
        if type(other) in (type(self), int):
            return super().__add__(other)
        else:
            return NotImplemented

    def __sub__(self, other: Any) -> Vector2i:
        if type(other) in (type(self), int):
            return super().__sub__(other)
        else:
            return NotImplemented

    def __mul__(self, other: Any) -> Vector2i:
        if type(other) in (type(self), int):
            return super().__mul__(other)
        else:
            return NotImplemented

    def __div__(self, other: Any) -> Vector2:
        if type(other) is int:
            return super().__truediv__(other)
        else:
            return NotImplemented


@dataclass
class Size(Vector2i):
    def __init__(self, width: int = 0, height: int = 0) -> None:
        super().__init__(width, height)

    @property
    def width(self) -> int:
        return self.x

    @property
    def height(self) -> int:
        return self.y

    @width.setter
    def width(self, value: int) -> None:
        self.x = value

    @height.setter
    def height(self, value: int) -> None:
        self.y = value
