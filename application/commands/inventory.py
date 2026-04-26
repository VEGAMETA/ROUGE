from application.commands.command import Command, CommandResult
from domain.entities.game_session import GameSession
from presentation.window import Window


class Inventory(Command):
    def execute(
        self, context: GameSession, window: Window, *args, **kwargs
    ) -> CommandResult:
        window.show_inventory(context)
        return CommandResult.NO_ACTION
