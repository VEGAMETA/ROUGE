from abc import ABC, abstractmethod
from typing import Any

from application.dto.game_state import GameStateDTO


class Renderer(ABC):
    def __init__(self) -> None:
        self.window: Any

    @abstractmethod
    def render(self, game_state: GameStateDTO) -> None: ...
