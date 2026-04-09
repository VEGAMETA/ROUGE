from abc import ABC

from application.dto.game_state import GameStateDTO


class Renderer(ABC):
    def render(self, game_state: GameStateDTO) -> None: ...


class Renderer2D(Renderer): ...


class Renderer3D(Renderer): ...
