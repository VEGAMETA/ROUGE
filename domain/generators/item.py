from random import choice, choices

from domain.entities.item import Item
from domain.entities.weapon import Weapon
from domain.rules.progression import Level
from domain.templates.item import ITEM_TEMPLATES
from domain.value_objects.position import Position
from domain.value_objects.stats import ItemRarityWeights


class ItemFactory:
    @staticmethod
    def create(key: tuple, position: Position, level: Level = Level.LEVEL_1) -> Item:
        item: Item = ITEM_TEMPLATES[key](position=position, level=level)

        if item is Weapon:
            w: dict[ItemRarityWeights, int] = ItemRarityWeights.get(level)
            item.rarity = choices(list(w.keys()), weights=list(w.values()))[0]
        return item

    @staticmethod
    def create_random(position: Position, level: Level = Level.LEVEL_1) -> Item:
        return ItemFactory.create(choice(list(ITEM_TEMPLATES.keys())), position, level)
