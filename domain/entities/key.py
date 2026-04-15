from dataclasses import dataclass

from domain.entities.door import Door
from domain.entities.entity import Entity2D


@dataclass(eq=False)
class Key(Entity2D):
    door: Door = None
