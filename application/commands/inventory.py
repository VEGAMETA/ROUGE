from application.commands.command import Command, CommandResult
from domain.entities.game_session import GameSession
from presentation.window import Window


class Inventory(Command):
    def execute(
        self, context: GameSession, window: Window, *args, **kwargs
    ) -> CommandResult:
        context
        window.notify("NA", "Menu", duration=2.0)
        return CommandResult.OK
