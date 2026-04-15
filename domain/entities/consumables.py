from dataclasses import dataclass

from domain.entities.entity import Character
from domain.entities.item import Item, ItemType
from domain.value_objects.enums import ConsumableType


@dataclass
class Consumable(Item, Character):
    type: ItemType = ItemType.CONSUMABLE
    subtype: ConsumableType = ConsumableType.UNDEFINED
