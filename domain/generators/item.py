from random import choice, choices

from domain.entities.item import Item
from domain.entities.weapon import Weapon
from domain.rules.progression import Level
from domain.templates.item import ITEM_TEMPLATES
from domain.value_objects.position import Position
from domain.value_objects.stats import ItemRarityWeights


class ItemFactory:
    @staticmethod
    def create(
        key: tuple,
        position: Position,
        level: Level = Level.LEVEL_1,
        template: dict = ITEM_TEMPLATES,
    ) -> Item:
        item: Item = template[key](position=position, level=level)
        if isinstance(item, Weapon):
            w: dict[ItemRarityWeights, int] = ItemRarityWeights.get(level)
            item.rarity = choices(list(w.keys()), weights=list(w.values()))[0]
            item.damage *= 1 + item.rarity.value * 0.1
        return item

    @staticmethod
    def create_random(
        position: Position,
        level: Level = Level.LEVEL_1,
        template: dict = ITEM_TEMPLATES,
    ) -> Item:
        return ItemFactory.create(
            choice(list(template.keys())),
            position,
            level,
            template,
        )
