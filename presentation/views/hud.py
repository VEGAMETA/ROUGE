from abc import ABC, abstractmethod
from typing import Any


class HUD(ABC):
    @abstractmethod
    def show(window: Any) -> None: ...
