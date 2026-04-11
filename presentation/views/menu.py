from abc import ABC, abstractmethod
from typing import Any


class Menu(ABC):
    @abstractmethod
    def show(window: Any) -> None: ...
