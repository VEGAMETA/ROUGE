from application.commands.command import Command, CommandResult
from domain.entities.game_session import GameSession
from domain.services.item import ItemService
from domain.value_objects.enums import ConsumableType, ItemType
from presentation.views.notificator import NotificationType
from presentation.window import Window


class UseElixir(Command):
    def execute(
        self, context: GameSession, window: Window, *args, **kwargs
    ) -> CommandResult:
        elixir = next(
            (
                item
                for item in context.player.inventory.items
                if item.type == ItemType.CONSUMABLE
                and item.subtype != ConsumableType.FOOD
            ),
            None,
        )
        if elixir is None:
            window.notify("No elixir", style=NotificationType.WARN)
            return CommandResult.NO_ACTION
        ItemService.use(elixir, context)
        return CommandResult.OK
