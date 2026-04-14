from dataclasses import dataclass

from domian.value_objects.vector import Vector2i


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
