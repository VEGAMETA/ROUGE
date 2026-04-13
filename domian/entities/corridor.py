from dataclasses import dataclass

from domian.value_objects.position import Position


@dataclass
class Corridor:
    path: list[Position]
