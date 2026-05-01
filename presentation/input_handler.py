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
    DROP: int = auto()
    INTERACT: int = auto()
    INVENTORY: int = auto()
    MENU: int = auto()
    QUIT: int = auto()
    USE_FOOD: int = auto()
    USE_WEAPON: int = auto()
    USE_ELIXIR: int = auto()
    USE_SCROLL: int = auto()


class InputHandler(ABC):
    LOCK: bool = False

    @staticmethod
    @abstractmethod
    def get(selected_3d: bool = False) -> InputAction: ...

    @staticmethod
    @abstractmethod
    def thread(window: Any) -> None: ...

    @staticmethod
    @abstractmethod
    def flush() -> None: ...
