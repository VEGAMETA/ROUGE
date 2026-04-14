from application.dto.game_state import GameStateDTO
from presentation.input_handler import InputAction, InputHandler
from presentation.renderer import Renderer
from presentation.views.notificator import NotificationType, Notificator


class Window:
    def __init__(
        self, renderer: Renderer, input_handler: InputHandler, notificator: Notificator
    ) -> None:
        self.renderer: Renderer = renderer
        self.input_handler: InputHandler = input_handler
        self.notificator: Notificator = notificator

    def get_size(self) -> tuple[int, int]: ...

    def _input(self) -> InputAction:
        return self.input_handler.get(self.window)

    def _draw(self, game_state: GameStateDTO) -> None:
        self.renderer.render(game_state)

    def _notify(
        self,
        message: str,
        title: str = "",
        duration: float = 0.0,
        style: NotificationType = NotificationType.UNDEFINED,
    ) -> None:
        self.notificator.show(self.window, message, title, duration, style)
        self.input_handler.flush()

    def close(self) -> None: ...

    def __del__(self) -> None:
        self.close()
