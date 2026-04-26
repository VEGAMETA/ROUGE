from dataclasses import dataclass

from domain.entities.entity import Entity2D
from domain.value_objects.enums import DoorSide, DoorType
from domain.value_objects.position import Position


@dataclass(eq=False)
class Door(Entity2D):
    position: Position
    side: DoorSide
    is_locked: bool = False
    type: DoorType = DoorType.OPENED
