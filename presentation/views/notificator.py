from abc import ABC, abstractmethod
from enum import IntEnum, auto
from typing import Any


class NotificationType(IntEnum):
    DEBUG: int = auto()
    INFO: int = auto()
    WARN: int = auto()
    ERROR: int = auto()
    OK: int = auto()


class Notificator(ABC):
    @staticmethod
    @abstractmethod
    def show(
        window: Any,
        message: str,
        title: str = "Notification",
        duration: float = 0.0,
        style: NotificationType = NotificationType.INFO,
    ) -> None: ...
