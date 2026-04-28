from abc import ABC, abstractmethod
from typing import Any


class LeaderboardView(ABC):
    @staticmethod
    @abstractmethod
    def show(window: Any, entries: list[str]) -> None: ...
