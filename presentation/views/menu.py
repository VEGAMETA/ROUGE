from abc import ABC, abstractmethod
from enum import IntEnum, auto
from typing import Any, Optional


class MenuAction(IntEnum):
    CONTINUE = auto()
    SAVE = auto()
    LOAD = auto()
    EXIT = auto()


class Menu(ABC):
    @staticmethod
    @abstractmethod
    def show(window: Any) -> Optional[MenuAction]: ...
