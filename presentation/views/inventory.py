from typing import Any

from application.dto.game_state import GameStateDTO


class InventoryView:
    @staticmethod
    def show(window: Any, context: GameStateDTO) -> None: ...
