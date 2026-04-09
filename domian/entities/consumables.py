from domian.entities.item import Item, ItemType
from domian.value_objects.enums import ConsumableType


class Consumables(Item):
    def __init__(
        self,
        subtype: ConsumableType = ConsumableType.UNDEFINED,
        health: int = 0,
        max_health: int = 0,
        dextrisity: int = 0,
        strength: int = 0,
        value: int = 0,
    ) -> None:
        super().__init__(ItemType.CONSUMABLE, subtype, value)
        self.health: int = health
        self.max_health: int = max_health
        self.dextrisity: int = dextrisity
        self.strength: int = strength
