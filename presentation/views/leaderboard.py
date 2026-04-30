from abc import ABC, abstractmethod
from typing import Any

from infrastructure.persistence.leaderboard import LeaderboardRecord


class LeaderboardView(ABC):
    @staticmethod
    @abstractmethod
    def show(window: Any, records: list[LeaderboardRecord]) -> None: ...
