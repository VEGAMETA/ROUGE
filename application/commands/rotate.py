from application.commands.command import Command, CommandResult
from domain.entities.game_session import GameSession


class Rotate(Command):
    def __init__(self, rotation_step: float) -> None:
        self.rotation_step = rotation_step

    def execute(self, context: GameSession, *args, **kwargs) -> CommandResult:
        context.player.rotation += self.rotation_step
        return CommandResult.NO_ACTION
