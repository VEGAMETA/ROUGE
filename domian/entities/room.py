from dataclasses import dataclass

from domian.entities.door import Door
from domian.value_objects.position import Position


@dataclass
class Room:
    position: Position
    width: int
    height: int
    doors: list[Door] = []
