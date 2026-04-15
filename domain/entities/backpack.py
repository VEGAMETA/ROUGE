from typing import Optional

from domain.entities.entity import Entity
from domain.entities.item import Item


class Backpack(Entity):
    def __init__(self, capacity: int = 3, items: list[Item] = []) -> None:
        super().__init__()
        self.capacity = capacity
        self.items = items

    def add_item(self, item: Item) -> None:
        if len(self.items) >= self.capacity:
            Exception("Backpack is full")
        self.items.append(item)

    def remove_item(self, item: Item) -> None:
        if item not in self.items:
            return
        self.items.remove(item)

    def pop_item(self, index: int = 0) -> Optional[Item]:
        if len(self.items) < index + 1:
            return
        self.items.pop(index)
