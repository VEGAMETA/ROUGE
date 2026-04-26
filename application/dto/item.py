from dataclasses import dataclass

from domain.entities.item import Item


@dataclass
class ItemDTO:
    x: int
    y: int
    type: int
    is_owned: bool
    name: str
    description: str
    value: int
    rarity: int


class ItemMapper:
    @staticmethod
    def to_dto(item: Item):
        return ItemDTO(
            x=item.position.x,
            y=item.position.y,
            type=item.type.value,
            is_owned=item.is_owned,
            name=item.name,
            description=item.description,
            value=item.value,
            rarity=item.rarity.value,
        )
