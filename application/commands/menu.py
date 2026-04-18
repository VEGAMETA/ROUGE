from application.commands.command import Command, CommandResult
from domain.entities.game_session import GameSession
from presentation.window import Window


class Menu(Command):
    def execute(
        self, context: GameSession, window: Window, *args, **kwargs
    ) -> CommandResult:
        context
        # window.notify("NA", "Menu", duration=2.0)
        window.show_menu(duration=2.0)
        return CommandResult.NO_ACTION
