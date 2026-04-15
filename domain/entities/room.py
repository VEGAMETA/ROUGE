from dataclasses import dataclass

from domain.entities.door import Door
from domain.entities.entity import Shape2D


@dataclass
class Room(Shape2D):
    doors: list[Door]
