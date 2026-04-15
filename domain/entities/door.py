from dataclasses import dataclass

from domain.entities.entity import Entity2D
from domain.value_objects.enums import DoorSide


@dataclass
class Door(Entity2D):
    side: DoorSide
    is_locked: bool = False
