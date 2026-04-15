from dataclasses import dataclass

from domain.entities.entity import Entity
from domain.value_objects.position import Position


@dataclass
class Corridor(Entity):
    path: list[Position]
