from random import choice, choices

from domain.entities.item import Item
from domain.rules.progression import Level
from domain.templates.item import ITEM_TEMPLATES
from domain.value_objects.position import Position
from domain.value_objects.stats import ItemRarityWeights


class ItemFactory:
    @staticmethod
    def create(key: tuple, position: Position, level: Level = Level.LEVEL_1) -> Item:
        weights = ItemRarityWeights.get(level)
        rarity = choices(list(weights.keys()), weights=list(weights.values()))[0]
        return ITEM_TEMPLATES[key](position=position, level=level, rarity=rarity)

    @staticmethod
    def create_random(position: Position, level: Level = Level.LEVEL_1) -> Item:
        return ItemFactory.create(choice(list(ITEM_TEMPLATES.keys())), position, level)
