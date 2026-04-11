from abc import ABC, abstractmethod

from application.dto.game_state import GameStateDTO


class Renderer(ABC):
    @abstractmethod
    def render(self, game_state: GameStateDTO) -> None: ...
