import curses

from infrastructure.timers import Timer
from presentation.curses.widgets import VerticalMenu
from presentation.views.menu import Menu


class CursesMenu(Menu):
    @staticmethod
    def show(window: curses.window, state: bool = False) -> None:
        curses.curs_set(0)
        window.clear()
        window.refresh()
        menu = VerticalMenu()
        menu.draw(window)
        if duration:
            Timer.sleep_for(duration)

