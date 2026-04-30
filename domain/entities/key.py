from dataclasses import dataclass

from domain.entities.entity import Entity2D
from domain.value_objects.enums import KeyType
from domain.value_objects.position import Position


@dataclass(eq=False)
class Key(Entity2D):
    type: KeyType = KeyType.RED
    position: Position = Position(0, 0)
