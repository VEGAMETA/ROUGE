from abc import ABC, abstractmethod
from enum import IntEnum, auto

from presentation.renderer import Renderer


class NotificationType(IntEnum):
    DEBUG: int = auto()
    INFO: int = auto()
    WARN: int = auto()
    ERROR: int = auto()
    OK: int = auto()


class Notification(ABC):
    @abstractmethod
    def show(
        renderer: Renderer,
        message: str,
        title: str = "Notification",
        duration: float = 0.0,
        style: NotificationType = NotificationType.INFO,
    ) -> None: ...
