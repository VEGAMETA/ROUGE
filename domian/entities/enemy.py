from dataclasses import dataclass

from domian.services.ai import EnemyAI
from domian.value_objects.enums import EnemyType, Hostility
from domian.value_objects.position import Position


@dataclass
class Enemy:
    type: EnemyType
    health: int
    dextrisity: int
    strength: int
    hostility: Hostility = Hostility.NEUTRAL
    ai: EnemyAI
    position: Position = Position()
    level: int = 0
