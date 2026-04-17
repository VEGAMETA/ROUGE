from dataclasses import dataclass

from domain.entities.entity import Character
from domain.value_objects.enums import EnemyType, Hostility


@dataclass(eq=False)
class Enemy(Character):
    type: EnemyType
    hostility: Hostility = Hostility.HOSTILE
