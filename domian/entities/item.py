from dataclasses import dataclass

from domian.rules.progression import Level
from domian.value_objects.enums import ItemRarityType, ItemType
from domian.value_objects.position import Position


@dataclass
class Item:
    type: ItemType = ItemType.UNDEFINED
    position: Position = Position()
    is_owned: bool = False
    name: str = ""
    description: str = ""
    value: int = 0
    level: Level = Level.LEVEL_1
    rarity: ItemRarityType = ItemRarityType.COMMON
