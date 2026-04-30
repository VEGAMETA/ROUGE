from dataclasses import dataclass
from typing import Optional

from domain.entities.corridor import Corridor
from domain.entities.entity import Shape2D
from domain.entities.key import Key
from domain.entities.room import Room


@dataclass
class Stage(Shape2D):
    corridors: list[Corridor]
    rooms: list[Room]
    keys: list[Key]
    graph: list[set[int]]
    start_room: Optional[Room] = None
    end_room: Optional[Room] = None
    MAX_ROOMS: int = 9
