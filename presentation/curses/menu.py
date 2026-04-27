import curses
from typing import Optional

from presentation.curses.widgets import Button, VerticalMenu
from presentation.views.menu import Menu, MenuAction

_ACTIONS = [MenuAction.CONTINUE, MenuAction.SAVE, MenuAction.LOAD, MenuAction.EXIT]


class CursesMenu(Menu):
    @staticmethod
    def show(window: curses.window) -> Optional[MenuAction]:
        curses.curs_set(0)
        menu = VerticalMenu(
            children=[
                Button(text="Continue"),
                Button(text="Save"),
                Button(text="Load"),
                Button(text="Exit"),
            ]
        )
        win = menu.draw(window)

        result: Optional[MenuAction] = MenuAction.CONTINUE
        while True:
            key = win.getch()
            if key == 27:
                result = MenuAction.CONTINUE
                break
            elif key in (ord("w"), curses.KEY_UP):
                menu.prev_widget()
                win = menu.draw(window)
            elif key in (ord("s"), curses.KEY_DOWN):
                menu.next_widget()
                win = menu.draw(window)
            elif key in (ord("e"), curses.KEY_ENTER, 10, 13):
                result = _ACTIONS[menu.children.index(menu.selected_widget)]
                break

        window.touchwin()
        window.refresh()
        return result
