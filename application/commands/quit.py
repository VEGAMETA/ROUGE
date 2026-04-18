from application.commands.command import Command
from domain.entities.game_session import GameSession


class Quit(Command):
    def execute(self, context: GameSession, *args, **kwargs):
        context.process = False
