from dataclasses import dataclass

from domian.entities.door import Door
from domian.entities.room import Room
from domian.value_objects.position import Position


@dataclass
class Corridor:
    path: list[Position]