from dataclasses import dataclass

from domian.entities.item import Item, ItemType
from domian.value_objects.enums import WeaponType


@dataclass
class Weapon(Item):
    type: ItemType = ItemType.WEAPON
    subtpe: WeaponType = WeaponType.UNDEFINED
    damage: int = 1
    required_dextrisity: int = 1
    required_strength: int = 1
    value: int = 0
