import abc
import enum


class ItemType(enum.Enum):
    UNDEFINED = 0
    CONSUMABLE = 1
    WEAPON = 2
    TREASURE = 3
    AMULET = 4


class Item(abc.ABC):
    def __init__(
        self,
        type_: ItemType = ItemType.UNDEFINED,
        subtype: int = 0,
        value: int = 0,
    ) -> None:
        self.type: ItemType = type_
        self.subtype: int = subtype
        self.value: int = value
