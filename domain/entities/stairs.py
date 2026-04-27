from dataclasses import dataclass

from domain.entities.entity import Entity2D
from domain.value_objects.enums import StairsType
from domain.value_objects.position import Position


@dataclass(eq=False)
class Stairs(Entity2D):
    position: Position
    type: StairsType = StairsType.DOWN
    explored: bool = True
