from application.commands.command import Command
from domain.entities.game_session import GameSession
from presentation.window import Window


class Menu(Command):
    def execute(self, context: GameSession, window: Window, *args, **kwargs):
        context
        window.notify("NA", "Menu", duration=2.0)
