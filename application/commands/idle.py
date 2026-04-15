from application.commands.command import Command, CommandResult


class Idle(Command):
    def __init__(self, pass_turn: bool = False) -> None:
        super().__init__()
        self.pass_turn = pass_turn

    def execute(self, *args, **kwargs) -> CommandResult:
        if self.pass_turn:
            return CommandResult.OK
        return CommandResult.NO_ACTION
