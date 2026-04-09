from dataclasses import dataclass

from domian.value_objects.enums import ItemType
from domian.value_objects.position import Position


@dataclass
class Item:
    type: ItemType = ItemType.UNDEFINED
    position: Position = Position()
    is_owned: bool = False
    name: str = ""
    description: str = ""
    value: int = 0
