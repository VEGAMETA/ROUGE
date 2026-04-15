from application.commands.command import Command
from domain.entities.game_session import GameSession
from presentation.window import Window


class Menu(Command):
    def execute(self, session: GameSession, window: Window, *args, **kwargs):
        session
        window.notify("NA", "Menu", duration=2.0)
