import curses
from typing import Any

from presentation.input_handler import InputAction, InputHandler


class CursesKeymap:
    ACTIONS: dict[str, InputAction] = {
        "q": InputAction.QUIT,
        "w": InputAction.MOVE_UP,
        "s": InputAction.MOVE_DOWN,
        "a": InputAction.MOVE_LEFT,
        "d": InputAction.MOVE_RIGHT,
        " ": InputAction.ATTACK,
        "e": InputAction.INTERACT,
        "\n": InputAction.INTERACT,
        "\011": InputAction.INVENTORY,
        "\033": InputAction.MENU,
    }


class CursesInputHandler(InputHandler):
    @staticmethod
    def get(window: Any) -> InputAction:
        if not isinstance(window, curses.window):
            return InputAction.UNDEFINED

        try:
            key = window.getkey()
        except KeyboardInterrupt:
            return InputAction.QUIT
        return CursesKeymap.ACTIONS.get(key, InputAction.UNDEFINED)

    @staticmethod
    def flush() -> None:
        curses.flushinp()
