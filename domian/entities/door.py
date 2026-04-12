from dataclasses import dataclass

from domian.value_objects.position import Position


@dataclass
class Door:
    position: Position
    side: str
    is_locked: bool = False