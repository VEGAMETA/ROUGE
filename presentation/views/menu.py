from abc import ABC, abstractmethod
from typing import Any


class Menu(ABC):
    @staticmethod
    @abstractmethod
    def show(window: Any, duration: float = 0.0) -> None: ...
