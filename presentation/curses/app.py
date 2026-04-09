import curses
from curses import window as CursesWindow

from application.globals import Globals


class Window:
    def __init__(self) -> None:
        self.window: CursesWindow = curses.initscr()
        Globals.set_window(self)

    def close(self) -> None:
        curses.endwin()
