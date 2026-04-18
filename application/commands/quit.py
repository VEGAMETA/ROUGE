from application.commands.command import Command, CommandResult
from domain.entities.game_session import GameSession


class Quit(Command):
    def execute(self, context: GameSession, *args, **kwargs) -> CommandResult:
        context.process = False
        return CommandResult.QUIT
