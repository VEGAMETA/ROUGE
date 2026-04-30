from dataclasses import dataclass

from domain.entities.entity import Character
from domain.value_objects.enums import EnemyType


@dataclass(eq=False)
class Enemy(Character):
    type: EnemyType
    path: list[tuple[int, int]]
    times_hit: int = 0
    resting: bool = False
    counter_queued: bool = False
    invisible: bool = False
    home_room_index: int = -1
    diagonal_dir: tuple = (1, 1)
    hostility: int = 0
