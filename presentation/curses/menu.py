import curses
from typing import Optional

from presentation.curses.input_handler import CursesInputHandler
from presentation.curses.widgets import Button, VerticalMenu
from presentation.input_handler import InputAction
from presentation.views.menu import Menu, MenuAction

_ACTIONS = [
    MenuAction.CONTINUE,
    MenuAction.LEADERBOARD,
    MenuAction.SAVE,
    MenuAction.LOAD,
    MenuAction.EXIT,
]


class CursesMenu(Menu):
    @staticmethod
    def show(window: curses.window) -> Optional[MenuAction]:
        curses.curs_set(0)
        menu = VerticalMenu(
            children=[
                Button(text="Continue"),
                Button(text="Leaderboard"),
                Button(text="Save"),
                Button(text="Load"),
                Button(text="Exit"),
            ]
        )
        menu.draw(window)

        result: Optional[MenuAction] = MenuAction.CONTINUE
        while True:
            key = CursesInputHandler.get(window)
            if key == InputAction.MENU:
                result = MenuAction.CONTINUE
                break
            elif key == InputAction.MOVE_UP:
                menu.prev_widget()
                menu.draw(window)
            elif key == InputAction.MOVE_DOWN:
                menu.next_widget()
                menu.draw(window)
            elif key == InputAction.INTERACT:
                result = _ACTIONS[menu.children.index(menu.selected_widget)]
                break

        window.touchwin()
        window.refresh()
        return result
