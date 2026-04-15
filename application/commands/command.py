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
    def execute(*args, **kwargs): ...


class CommandService:
    commands: dict[InputAction, Command] = {}

    def __init__(
        self, action: InputAction, session: GameSession, window: Window
    ) -> None:
        self.action: InputAction = action
        self.session: GameSession = session
        self.window: Window = window

    @classmethod
    def register(cls, input_action: InputAction, command: Command):
        cls.commands[input_action] = command

    def execute(self, *args, **kwargs):
        self.commands[self.action]().execute(self.session, self.window)

        # match self.action:
        #     case InputAction.QUIT:
        #         self.session.process = False
        #     case InputAction.MENU:
        #         self.window.notify("NA", "Menu", duration=2.0)
        #     case action if action in MOVE_COMMAND:
        #         MovementService.move(self.session, MOVE_COMMAND[self.action])
        #     case InputAction.ATTACK:
        #         CombatService

        # return Exit.OK
