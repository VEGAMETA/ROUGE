from dataclasses import dataclass

from domian.value_objects.enums import DoorSide
from domian.value_objects.position import Position


@dataclass
class Door:
    position: Position
    side: DoorSide
    is_locked: bool = False
