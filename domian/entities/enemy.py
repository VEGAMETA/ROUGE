from dataclasses import dataclass

from domian.rules.progression import Level
from domian.services.ai import EnemyAI
from domian.value_objects.enums import EnemyType, Hostility
from domian.value_objects.position import Position


@dataclass
class Enemy:
    type: EnemyType
    ai: EnemyAI
    health: int
    dexterity: int
    strength: int
    position: Position = Position()
    hostility: Hostility = Hostility.HOSTILE
    level: Level = Level.LEVEL_1
