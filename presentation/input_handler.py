from abc import ABC, abstractmethod
from enum import IntEnum, auto
from typing import Any


class InputAction(IntEnum):
    UNDEFINED: int = auto()
    MOVE_UP: int = auto()
    MOVE_DOWN: int = auto()
    MOVE_LEFT: int = auto()
    MOVE_RIGHT: int = auto()
    ROTATE_LEFT: int = auto()
    ROTATE_RIGHT: int = auto()
    PASS: int = auto()
    INTERACT: int = auto()
    INVENTORY: int = auto()
    MENU: int = auto()
    QUIT: int = auto()


class InputHandler(ABC):
    LOCK: bool = False

    @staticmethod
    @abstractmethod
    def get(window: Any) -> InputAction: ...

    @staticmethod
    @abstractmethod
    def flush(self) -> None: ...
