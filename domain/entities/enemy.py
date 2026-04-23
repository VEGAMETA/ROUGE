from dataclasses import dataclass

from domain.entities.entity import Character
from domain.value_objects.enums import EnemyType, Hostility


@dataclass(eq=False)
class Enemy(Character):
    type: EnemyType
    path: list[tuple[int, int]]
    hostility: Hostility = Hostility.HOSTILE
