from dataclasses import dataclass
from typing import Any

from domain.entities.entity import Entity2D
from domain.rules.progression import Level
from domain.value_objects.enums import ItemRarityType, ItemType


@dataclass(eq=False)
class Item(Entity2D):
    type: ItemType = ItemType.UNDEFINED
    subtype: Any = ItemType.UNDEFINED
    is_owned: bool = False
    name: str = ""
    description: str = ""
    value: int = 0
    level: Level = Level.LEVEL_1
    rarity: ItemRarityType = ItemRarityType.COMMON
