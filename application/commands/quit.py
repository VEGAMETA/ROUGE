from application.commands.command import Command
from domain.entities.game_session import GameSession


class Quit(Command):
    def execute(self, session: GameSession, *args, **kwargs):
        session.process = False
