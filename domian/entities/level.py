from dataclasses import dataclass

from domian.entities.corridor import Corridor
from domian.entities.room import Room


@dataclass
class Level:
    rooms: rooms = list[Room]
    corridors: corridors = list[Corridor]