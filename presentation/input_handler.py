from abc import ABC, abstractmethod
from enum import IntEnum, auto

from presentation.renderer import Renderer


class InputAction(IntEnum):
    UNDEFINED: int = auto()
    QUIT: int = auto()
    MOVE_UP: int = auto()
    MOVE_DOWN: int = auto()
    MOVE_LEFT: int = auto()
    MOVE_RIGHT: int = auto()
    ATTACK: int = auto()
    MENU: int = auto()
    INVENTORY: int = auto()
    INTERRACT: int = auto()
    PICKUP: int = auto()
    DROP: int = auto()


class InputHandler(ABC):
    @abstractmethod
    def __init__(self, renderer: Renderer) -> None: ...

    @abstractmethod
    def get(self) -> InputAction: ...
