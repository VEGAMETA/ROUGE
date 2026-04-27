import curses

from presentation.curses.input_handler import CursesInputHandler
from presentation.curses.inventory import CursesInventoryView
from presentation.curses.menu import CursesMenu
from presentation.curses.notificator import CursesNotificator
from presentation.curses.render.renderer2d import CursesRenderer2D
from presentation.curses.render.renderer3d import CursesRenderer3D
from presentation.window import Window


class CursesWindow(Window):
    @staticmethod
    def _get_curses_window(window: curses.window) -> curses.window:
        return window

    def __init__(self, selected_3d: bool = False):
        super().__init__(
            CursesRenderer3D() if selected_3d else CursesRenderer2D(),
            CursesInputHandler,
            CursesNotificator,
            CursesMenu,
            CursesInventoryView,
        )
        # import os

        # os.environ["ESCDELAY"] = "1"
        self.window: curses.window = curses.wrapper(self._get_curses_window)
        self.renderer.window = self.window
        self.window.clear()
        self.window.refresh()
        self.window.nodelay(True)
        self.window.keypad(True)
        self.window.timeout(0)
        curses.start_color()
        curses.typeahead(-1)
        curses.noqiflush()
        curses.curs_set(0)
        curses.cbreak()
        curses.noecho()
        if hasattr(curses, "set_escdelay"):
            curses.set_escdelay(1)
        # curses.raw()

    def get_size(self) -> tuple[int, int]:
        return self.window.getmaxyx()[::-1]

    def close(self) -> None:
        curses.echo()
        self.window.clear()
        self.window.refresh()
        curses.nocbreak()
        self.window.keypad(False)
        curses.use_default_colors()
        curses.endwin()
