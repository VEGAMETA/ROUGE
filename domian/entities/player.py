from dataclasses import dataclass

from domian.entities.backpack import Backpack
from domian.entities.weapon import Weapon
from domian.value_objects.position import Position


@dataclass
class Player:
    position: Position
    health: int = 5
    max_health: int = 5
    dextrisity: int = 1
    strength: int = 1
    weapon: Weapon | None = None
    inventory: Backpack = Backpack()
    level: int = 0
