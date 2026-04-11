from dataclasses import dataclass

from domian.entities.door import Door
from domian.value_objects.position import Position


@dataclass
class Key:
    position: Position
    door: Door = None
