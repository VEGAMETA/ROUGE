from dataclasses import dataclass

from domian.entities.corridor import Corridor
from domian.entities.room import Room


@dataclass
class Stage:
    rooms: list[Room]
    corridors: list[Corridor]
    width: int
    height: int
    graph: list[set[int]]
    MAX_ROOMS: int = 9
