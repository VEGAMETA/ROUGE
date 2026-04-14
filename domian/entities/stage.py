from dataclasses import dataclass

from domian.entities.corridor import Corridor
from domian.entities.room import Room


@dataclass
class Stage:
    width: int
    height: int
    corridors: list[Corridor]
    rooms: list[Room]
    graph: list[set[int]]
    MAX_ROOMS: int = 9
