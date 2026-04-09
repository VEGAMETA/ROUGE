from dataclasses import dataclass

from domian.entities.item import Item, ItemType
from domian.value_objects.enums import ConsumableType


@dataclass
class Consumable(Item):
    type: ItemType = ItemType.CONSUMABLE
    subtype: ConsumableType = ConsumableType.UNDEFINED
    health: int = 0
    max_health: int = 0
    dextrisity: int = 0
    strength: int = 0
