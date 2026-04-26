from dataclasses import dataclass

from domain.entities.item import Item, ItemType
from domain.value_objects.enums import ConsumableType


@dataclass(eq=False)
class Scroll(Item):
    type: ItemType = ItemType.SCROLL
    subtype: ConsumableType = ConsumableType.UNDEFINED
    health: int = 0
    max_health: int = 0
    dexterity: int = 0
    strength: int = 0
