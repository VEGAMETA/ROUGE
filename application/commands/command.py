from abc import ABC, abstractmethod
from enum import IntEnum, auto

from domain.entities.game_session import GameSession
from presentation.input_handler import InputAction
from presentation.window import Window


class CommandResult(IntEnum):
    OK: int = auto()
    ERROR: int = auto()
    SWAP_ACTION: int = auto()
    NO_ACTION: int = auto()
    QUIT: int = auto()


class Command(ABC):
    @staticmethod
    @abstractmethod
    def execute(*args, **kwargs) -> CommandResult: ...


class CommandService:
    commands: dict[InputAction, Command] = {}

    def __init__(
        self, action: InputAction, context: GameSession, window: Window
    ) -> None:
        self.action: InputAction = action
        self.context: GameSession = context
        self.window: Window = window

    @classmethod
    def register(cls, input_action: InputAction, command: Command):
        cls.commands[input_action] = command

    def execute(self, *args, **kwargs) -> CommandResult:
        return self.commands[self.action]().execute(self.context, self.window)
