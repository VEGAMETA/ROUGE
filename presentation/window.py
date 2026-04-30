from typing import Any, Optional

from application.dto.game_state import GameStateDTO
from domain.entities.statistics import Statistics
from infrastructure.persistence.leaderboard import LeaderboardRecord
from presentation.input_handler import InputAction, InputHandler
from presentation.renderer import Renderer
from presentation.views.inventory import InventoryView
from presentation.views.leaderboard import LeaderboardView
from presentation.views.menu import Menu, MenuAction
from presentation.views.notificator import NotificationType, Notificator
from presentation.views.summary import RunSummary


class Window:
    def __init__(
        self,
        renderer: Renderer,
        input_handler: InputHandler,
        notificator: Notificator,
        menu: Menu,
        inventory_view: InventoryView,
        leaderboard_view: LeaderboardView,
    ) -> None:
        self.renderer: Renderer = renderer
        self.input_handler: InputHandler = input_handler
        self.notificator: Notificator = notificator
        self.menu: Menu = menu
        self.inventory_view: InventoryView = inventory_view
        self.leaderboard_view: LeaderboardView = leaderboard_view
        self.window: Any = None

    def get_size(self) -> tuple[int, int]: ...

    def action(self, selected_3d: bool = False) -> InputAction:
        return self.input_handler.get(self.window, selected_3d)

    def draw(self, context: GameStateDTO, tick_time: float) -> None:
        self.renderer.render(context, tick_time)

    def notify(
        self,
        message: str,
        title: str = "",
        duration: float = 0.0,
        style: NotificationType = NotificationType.UNDEFINED,
    ) -> None:
        self.notificator.show(self.window, message, title, duration, style)
        self.input_handler.flush()

    def show_menu(self) -> Optional[MenuAction]:
        result = self.menu.show(self.window)
        self.input_handler.flush()
        return result

    def show_inventory(self, context: GameStateDTO) -> None:
        self.inventory_view.show(self.window, context)
        self.input_handler.flush()

    def show_leaderboard(self, records: list[LeaderboardRecord]) -> None:
        self.leaderboard_view.show(self.window, records)
        self.input_handler.flush()

    TITLE_GAME_OVER: str = "GAME OVER ☠"
    TITLE_VICTORY: str = "VICTORY ♚"

    def game_over(self, time: float, statistics: Statistics, points: int) -> None:
        self.notificator.show(
            self.window,
            RunSummary.format(statistics, points, time),
            Window.TITLE_GAME_OVER,
            0.0,
            NotificationType.ERROR,
        )

    def victory(self, time: float, statistics: Statistics, points: int) -> None:
        self.notificator.show(
            self.window,
            RunSummary.format(statistics, points, time),
            Window.TITLE_VICTORY,
            0.0,
            NotificationType.OK,
        )

    def close(self) -> None: ...

    def __del__(self) -> None:
        self.close()
