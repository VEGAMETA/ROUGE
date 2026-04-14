from dataclasses import dataclass

from domian.entities.item import Item, ItemType
from domian.value_objects.enums import WeaponType


@dataclass
class Weapon(Item):
    type: ItemType = ItemType.WEAPON
    subtype: WeaponType = WeaponType.UNDEFINED
    damage: int = 1
    required_dexterity: int = 1
    required_strength: int = 1
    value: int = 0
