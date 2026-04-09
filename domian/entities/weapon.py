from domian.entities.item import Item, ItemType
from domian.value_objects.enums import WeaponType


class Weapon(Item):
    def __init__(
        self,
        subtype: WeaponType = 0,
        damage: int = 1,
        required_dextrisity: int = 1,
        required_strength: int = 1,
        value: int = 0,
    ) -> None:
        super().__init__(ItemType.WEAPON, subtype, value)
        self.damage: int = damage
        self.required_dextrisity: int = required_dextrisity
        self.required_strength: int = required_strength
        self.value: int = value
