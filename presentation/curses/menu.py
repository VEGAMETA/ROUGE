import curses

from presentation.views.menu import Menu


class CursesMenu(Menu):
    def show(window: curses.window) -> None: ...
