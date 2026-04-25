from application.commands.command import Command, CommandResult
from domain.entities.game_session import GameSession
from domain.services.item import ItemService
from domain.value_objects.enums import ConsumableType, ItemType
from presentation.views.notificator import NotificationType
from presentation.window import Window


class EatFood(Command):
    def execute(
        self, context: GameSession, window: Window, *args, **kwargs
    ) -> CommandResult:
        food = next(
            (
                item
                for item in context.player.inventory.items
                if item.type == ItemType.CONSUMABLE
                and item.subtype == ConsumableType.FOOD
            ),
            None,
        )
        if food is None:
            window.notify("No food", style=NotificationType.WARN)
            return CommandResult.NO_ACTION
        ItemService.use(food, context)
        return CommandResult.OK
