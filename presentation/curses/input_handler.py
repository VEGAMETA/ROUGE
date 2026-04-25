import _curses
import curses

from presentation.input_handler import InputAction, InputHandler


def unite_dicts(dict1: dict, dict2: dict) -> dict:
    result = dict1.copy()
    result.update(dict2)
    return result


class CursesKeymap:
    BASE_ACTIONS: dict[int, InputAction] = {
        ord("q"): InputAction.QUIT,
        ord("j"): InputAction.USE_FOOD,
        ord("k"): InputAction.USE_ELIXIR,
        ord("h"): InputAction.USE_WEAPON,
        ord("e"): InputAction.INTERACT,
        curses.KEY_ENTER: InputAction.INTERACT,
        9: InputAction.INVENTORY,
        32: InputAction.PASS,
        27: InputAction.MENU,
    }

    ACTIONS: dict[int, InputAction] = unite_dicts(
        BASE_ACTIONS,
        {
            ord("w"): InputAction.MOVE_UP,
            ord("s"): InputAction.MOVE_DOWN,
            ord("a"): InputAction.MOVE_LEFT,
            ord("d"): InputAction.MOVE_RIGHT,
            curses.KEY_UP: InputAction.MOVE_UP,
            curses.KEY_DOWN: InputAction.MOVE_DOWN,
            curses.KEY_LEFT: InputAction.MOVE_LEFT,
            curses.KEY_RIGHT: InputAction.MOVE_RIGHT,
        },
    )

    ACTIONS_3D: dict[int, InputAction] = unite_dicts(
        BASE_ACTIONS,
        {
            ord("w"): InputAction.MOVE_UP,
            ord("s"): InputAction.MOVE_DOWN,
            ord("a"): InputAction.ROTATE_LEFT,
            ord("d"): InputAction.ROTATE_RIGHT,
            curses.KEY_UP: InputAction.MOVE_UP,
            curses.KEY_DOWN: InputAction.MOVE_DOWN,
            curses.KEY_LEFT: InputAction.ROTATE_LEFT,
            curses.KEY_RIGHT: InputAction.ROTATE_RIGHT,
        },
    )


class CursesInputHandler(InputHandler):
    @staticmethod
    def get(window: curses.window, action3d: bool = False) -> InputAction:
        if not isinstance(window, curses.window):
            return InputAction.UNDEFINED

        try:
            key = window.get_wch()
            CursesInputHandler.flush()
        except KeyboardInterrupt:
            return InputAction.QUIT
        except _curses.error:
            return InputAction.UNDEFINED

        actions = CursesKeymap.ACTIONS_3D if action3d else CursesKeymap.ACTIONS
        return actions.get(
            ord(key) if isinstance(key, str) else key, InputAction.UNDEFINED
        )

    @staticmethod
    def flush() -> None:
        curses.flushinp()
