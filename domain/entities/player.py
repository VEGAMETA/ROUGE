from dataclasses import dataclass
from typing import Optional

from domain.entities.backpack import Backpack
from domain.entities.entity import Character
from domain.entities.weapon import Weapon
from domain.value_objects.position import Direction


@dataclass(eq=False)
class Player(Character):
    temp_strength: int = 0
    temp_dexterity: int = 0
    temp_max_health: int = 0
    weapon: Optional[Weapon] = None
    inventory: Backpack = Backpack()
    rotation: float = -3.14159 / 2.0
    direction: Direction = Direction.UP
