from dataclasses import dataclass

from domain.entities.item import Item
from domain.value_objects.enums import ItemType


@dataclass
class ItemDTO:
    x: int
    y: int
    type: ItemType
    is_owned: bool
    name: str
    description: str
    value: int


class ItemMapper:
    @staticmethod
    def to_dto(item: Item):
        return ItemDTO(
            x=item.position.x,
            y=item.position.y,
            type=item.type,
            is_owned=item.is_owned,
            name=item.name,
            description=item.description,
            value=item.value,
        )
