import curses

from presentation.curses.input_handler import CursesInputHandler
from presentation.curses.menu import CursesMenu
from presentation.curses.notificator import CursesNotificator
from presentation.curses.renderer import CursesRenderer2D
from presentation.window import Window


class CursesWindow(Window):
    def __init__(self):
        super().__init__(
            CursesRenderer2D(), CursesInputHandler, CursesNotificator, CursesMenu
        )
        self.window: curses.window = curses.initscr()
        self.renderer.window = self.window
        self.window.clear()
        self.window.refresh()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self.window.keypad(True)

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
