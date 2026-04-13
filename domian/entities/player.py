from dataclasses import dataclass

from domian.entities.backpack import Backpack
from domian.entities.weapon import Weapon
from domian.rules.progression import Level
from domian.value_objects.position import Position
from domian.value_objects.rotation import Rotation


@dataclass
class Player:
    position: Position
    rotation: Rotation
    health: int = 5
    max_health: int = 5
    dextrisity: int = 1
    strength: int = 1
    weapon: Weapon | None = None
    inventory: Backpack = Backpack()
    level: Level = Level.LEVEL_1
