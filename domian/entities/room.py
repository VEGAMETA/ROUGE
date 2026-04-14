from dataclasses import dataclass

from domian.entities.door import Door
from domian.value_objects.position import Position
from domian.value_objects.size import Size


@dataclass
class Room:
    position: Position
    size: Size
    doors: list[Door]
