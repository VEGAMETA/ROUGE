import curses

from infrastructure.timers import Timer
from presentation.curses.widgets import Button, Checkbox, Label, Slider, VerticalMenu
from presentation.views.menu import Menu


class CursesMenu(Menu):
    @staticmethod
    def show(window: curses.window, duration: float = 0.0) -> None:
        curses.curs_set(0)
        # window.clear()
        # window.refresh()
        menu = VerticalMenu(
            children=[
                Label(text="Continue"),
                Button(text="Exit"),
                Checkbox(text="3d"),
                Slider(text="Sound"),
            ]
        )
        menu.draw(window)
        if duration:
            Timer.sleep_for(duration)
        # window.clear()
        window.refresh()

    def hide(window: curses.window) -> None: ...
