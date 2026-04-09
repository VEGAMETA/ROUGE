import enum

from classes.items.item import Item, ItemType


class ConsumableType(enum.Enum):
    UNDEFINED = 0
    HEALTH = 1
    DEXTRISITY = 2
    STRENGTH = 3
    MAX_HEALTH = 4
    MAX_DEXTRISITY = 5
    MAX_STRENGTH = 6


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
