from dataclasses import dataclass

from domian.entities.corridor import Corridor
from domian.entities.room import Room
from domian.value_objects.size import Size


@dataclass
class Stage:
    size: Size
    corridors: list[Corridor]
    rooms: list[Room]
    graph: list[set[int]]
    MAX_ROOMS: int = 9
