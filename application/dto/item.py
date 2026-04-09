from dataclasses import dataclass

from domian.entities.item import Item
from domian.value_objects.enums import ItemType


@dataclass
class ItemDTO:
    type: ItemType
    is_owned: bool
    name: str
    description: str
    value: int


class ItemMapper:
    @staticmethod
    def to_dto(item: Item):
        return ItemDTO(
            type=item.type,
            is_owned=item.is_owned,
            name=item.name,
            description=item.description,
            value=item.value,
        )
