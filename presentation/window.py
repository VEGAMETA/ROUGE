from typing import Any

from application.dto.game_state import GameStateDTO
from presentation.input_handler import InputAction, InputHandler
from presentation.renderer import Renderer
from presentation.views.inventory import InventoryView
from presentation.views.menu import Menu
from presentation.views.notificator import NotificationType, Notificator


class Window:
    def __init__(
        self,
        renderer: Renderer,
        input_handler: InputHandler,
        notificator: Notificator,
        menu: Menu,
        inventory_view: InventoryView,
    ) -> None:
        self.renderer: Renderer = renderer
        self.input_handler: InputHandler = input_handler
        self.notificator: Notificator = notificator
        self.menu: Menu = menu
        self.inventory_view: InventoryView = inventory_view
        self.window: Any = None

    def get_size(self) -> tuple[int, int]: ...

    def action(self, action3d: bool = False) -> InputAction:
        return self.input_handler.get(self.window, action3d)

    def draw(self, context: GameStateDTO) -> None:
        self.renderer.render(context)

    def notify(
        self,
        message: str,
        title: str = "",
        duration: float = 0.0,
        style: NotificationType = NotificationType.UNDEFINED,
    ) -> None:
        self.notificator.show(self.window, message, title, duration, style)
        self.input_handler.flush()

    def show_menu(self, duration: float = 0.0) -> None:
        self.menu.show(self.window, duration)
        self.input_handler.flush()

    def show_inventory(self, context: GameStateDTO) -> None:
        self.inventory_view.show(self.window, context)
        self.input_handler.flush()

    def game_over(self, time: float) -> None:
        self.notificator.show(
            self.window, "GAME OVER", f"{time:.2f}", 0.0, NotificationType.ERROR
        )

    def close(self) -> None: ...

    def __del__(self) -> None:
        self.close()
