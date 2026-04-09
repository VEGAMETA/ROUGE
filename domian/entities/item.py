import abc

from domian.value_objects.enums import ItemType


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
