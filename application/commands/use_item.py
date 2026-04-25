from application.commands.command import Command, CommandResult
from domain.entities.game_session import GameSession
from domain.services.item import ItemService
from domain.value_objects.enums import ItemType, SoundType
from presentation.curses.backpack import CursesBackpackView
from presentation.window import Window


class UseItem(Command):
    def __init__(self, item_type: ItemType) -> None:
        self.item_type = item_type

    def execute(
        self, context: GameSession, window: Window, *args, **kwargs
    ) -> CommandResult:
        items = [
            item
            for item in context.player.inventory.items
            if item.type == self.item_type
        ]
        equipped = context.player.weapon if self.item_type == ItemType.WEAPON else None
        idx = window.show_backpack(items, self.item_type, equipped)
        if idx is None:
            return CommandResult.NO_ACTION
        if idx == -1:
            context.player.weapon = None
            context.sounds.put(SoundType.ITEM_USE)
            return CommandResult.NO_ACTION
        if idx >= CursesBackpackView.DROP_OFFSET:
            item = items[idx - CursesBackpackView.DROP_OFFSET]
            if context.player.weapon is item:
                context.player.weapon = None
            context.player.inventory.remove_item(item)
            return CommandResult.NO_ACTION
        ItemService.use(items[idx], context)
        return (
            CommandResult.NO_ACTION
            if self.item_type == ItemType.WEAPON
            else CommandResult.OK
        )
