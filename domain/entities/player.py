from dataclasses import dataclass
from typing import Optional

from domain.entities.backpack import Backpack
from domain.entities.entity import Character
from domain.entities.weapon import Weapon
from domain.value_objects.position import Direction
from domain.value_objects.rotation import Rotation


@dataclass(eq=False)
class Player(Character):
    weapon: Optional[Weapon] = None
    inventory: Backpack = Backpack()
    rotation: Rotation = Rotation()
    direction: Direction = Direction.UP
