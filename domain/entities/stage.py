from dataclasses import dataclass

from domain.entities.corridor import Corridor
from domain.entities.entity import Shape2D
from domain.entities.room import Room


@dataclass
class Stage(Shape2D):
    corridors: list[Corridor]
    rooms: list[Room]
    graph: list[set[int]]
    MAX_ROOMS: int = 9
