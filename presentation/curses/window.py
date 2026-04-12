from presentation.curses.input_handler import CursesInputHandler
from presentation.curses.notificator import CursesNotificator
from presentation.curses.renderer import CursesRenderer2D
from presentation.window import Window


class CursesWindow(Window):
    def __init__(self):
        super().__init__(CursesRenderer2D(), CursesInputHandler, CursesNotificator)
