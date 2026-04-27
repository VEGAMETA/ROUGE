from application.commands.command import Command, CommandResult
from domain.entities.game_session import GameSession
from domain.services.item import ItemService
from domain.value_objects.enums import ItemType
from presentation.views.notificator import NotificationType
from presentation.window import Window


class UseScroll(Command):
    def execute(
        self, context: GameSession, window: Window, *args, **kwargs
    ) -> CommandResult:
        scroll = next(
            (
                item
                for item in context.player.inventory.items
                if item.type == ItemType.SCROLL
            ),
            None,
        )
        if scroll is None:
            window.notify("No scroll", style=NotificationType.WARN)
            return CommandResult.NO_ACTION
        ItemService.use(scroll, context)
        return CommandResult.OK
