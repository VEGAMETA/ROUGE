from dataclasses import dataclass

from domian.rules.progression import Level
from domian.services.ai import EnemyAI
from domian.value_objects.enums import EnemyType, Hostility
from domian.value_objects.position import Position


@dataclass
class Enemy:
    type: EnemyType
    position: Position = Position()
    hostility: Hostility = Hostility.HOSTILE
    ai: EnemyAI
    health: int
    dextrisity: int
    strength: int
    level: Level = Level.LEVEL_1
