from domain.entities.game_session import GameSession
from domain.entities.item import Item
from domain.value_objects.enums import ConsumableType, ItemType, SoundType

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
    def pickup(item: Item, context: GameSession) -> bool:
        inv = context.player.inventory.items

        if item.type == ItemType.TREASURE:
            context.points += item.value
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
            return True

        if ItemService._count_type(inv, item) >= _PER_TYPE_LIMIT:
            return False

        item.is_owned = True
        context.player.inventory.add_item(item)
        return True

    @staticmethod
    def use(item: Item, context: GameSession) -> bool:
        if item.type == ItemType.CONSUMABLE:
            ItemService._apply_consumable(item, context)
            if item.subtype == ConsumableType.FOOD and item.count > 1:
                item.count -= 1
            else:
                context.player.inventory.remove_item(item)
        elif item.type == ItemType.SCROLL:
            ItemService._apply_consumable(item, context)
            context.player.inventory.remove_item(item)
        elif item.type == ItemType.WEAPON:
            context.player.weapon = item
        context.sounds.put(SoundType.ITEM_USE)
        return True

    @staticmethod
    def _apply_consumable(item: Item, context: GameSession) -> None:
        match item.subtype:
            case ConsumableType.HEALTH | ConsumableType.FOOD:
                context.player.health = min(
                    context.player.health + item.health, context.player.max_health
                )
            case ConsumableType.STRENGTH | ConsumableType.MAX_STRENGTH:
                context.player.strength += item.strength
            case ConsumableType.DEXTERITY | ConsumableType.MAX_DEXTERITY:
                context.player.dexterity += item.dexterity
            case ConsumableType.MAX_HEALTH:
                context.player.max_health += item.max_health
                context.player.health += item.max_health
