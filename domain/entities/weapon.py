from dataclasses import dataclass

from domain.entities.item import Item, ItemType
from domain.value_objects.enums import WeaponType


@dataclass(eq=False)
class Weapon(Item):
    type: ItemType = ItemType.WEAPON
    subtype: WeaponType = WeaponType.UNDEFINED
    damage: int = 1
    required_dexterity: int = 1
    required_strength: int = 1
    equiped: bool = False
