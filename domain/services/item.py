from random import choice

from domain.entities.consumables import Consumable
from domain.entities.game_session import GameSession
from domain.entities.item import Item
from domain.entities.key import Key
from domain.value_objects.enums import ConsumableType, ItemType, SoundType
from domain.value_objects.position import Position

_PER_TYPE_LIMIT = 9


class ItemService:
    @staticmethod
    def _count_type(items: list[Item], item: Item) -> int:
        if item.type == ItemType.CONSUMABLE:
            return sum(
                1
                for i in items
                if i.type == ItemType.CONSUMABLE and i.subtype != ConsumableType.FOOD
            )
        return sum(1 for i in items if i.type == item.type)

    @staticmethod
    def pickup_key(key: Key, context: GameSession) -> bool:
        context.owned_keys.append(key)
        context.keys.remove(key)
        return True

    @staticmethod
    def pickup(item: Item, context: GameSession) -> bool:
        inv = context.player.inventory.items

        if item.type == ItemType.TREASURE:
            context.points += item.value
            context.statistics.treasure_collected += item.value
            item.is_owned = True
            return True

        if item.type == ItemType.CONSUMABLE and item.subtype == ConsumableType.FOOD:
            existing = next(
                (
                    i
                    for i in inv
                    if i.type == ItemType.CONSUMABLE
                    and i.subtype == ConsumableType.FOOD
                ),
                None,
            )
            if existing is not None:
                if existing.count >= _PER_TYPE_LIMIT:
                    return False
                existing.count += 1
                item.is_owned = True
                return True
            item.count = 1
            item.is_owned = True
            context.player.inventory.add_item(item)
            context.points += item.value
            return True

        if ItemService._count_type(inv, item) >= _PER_TYPE_LIMIT:
            return False

        item.is_owned = True
        context.player.inventory.add_item(item)
        return True

    @staticmethod
    def drop(item: Item, context: GameSession) -> bool:
        positions: list[Position] = []
        for x in range(context.player.position.x - 1, context.player.position.x + 2):
            for y in range(
                context.player.position.y - 1, context.player.position.y + 2
            ):
                if context.cached_obstacle_map[y][x]:
                    continue
                if x == context.player.position.x and y == context.player.position.y:
                    continue
                positions.append(Position(x, y))
        drop_pos = choice(positions)
        item.position = drop_pos
        item.is_owned = False
        item.value = 0
        context.items.append(item)

    @staticmethod
    def use(item: Item, context: GameSession) -> bool:
        if item.type == ItemType.CONSUMABLE:
            ItemService._apply_consumable(item, context, True)
            if item.subtype == ConsumableType.FOOD and item.count > 1:
                item.count -= 1
            else:
                context.player.inventory.remove_item(item)
            if item.subtype == ConsumableType.FOOD:
                context.statistics.food_consumed += 1
            else:
                context.statistics.elixirs_used += 1
        elif item.type == ItemType.SCROLL:
            ItemService._apply_consumable(item, context)
            context.player.inventory.remove_item(item)
            context.statistics.scrolls_read += 1
        elif item.type == ItemType.WEAPON:
            context.player.weapon = item
        context.sounds.put(SoundType.ITEM_USE)
        return True

    @staticmethod
    def _apply_consumable(
        item: Consumable, context: GameSession, temporarily: bool = False
    ) -> None:
        match item.subtype:
            case ConsumableType.FOOD | ConsumableType.HEALTH:
                context.player.health = min(
                    context.player.health + item.health, context.player.max_health
                )
            case ConsumableType.STRENGTH:
                context.player.strength += item.strength
                context.player.temp_strength += temporarily * item.strength
            case ConsumableType.DEXTERITY:
                context.player.dexterity += item.dexterity
                context.player.temp_dexterity += temporarily * item.dexterity
            case ConsumableType.MAX_HEALTH:
                context.player.max_health += item.max_health
                context.player.health = context.player.max_health
                context.player.temp_max_health += temporarily * item.max_health
