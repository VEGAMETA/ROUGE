import _curses
import curses

from presentation.input_handler import InputAction, InputHandler


def unite_dicts(dict1: dict, dict2: dict) -> dict:
    result = dict1.copy()
    result.update(dict2)
    return result


class CursesKeymap:
    BASE_ACTIONS: dict[int, InputAction] = {
        ord("h"): InputAction.USE_WEAPON,
        ord("H"): InputAction.USE_WEAPON,
        ord("j"): InputAction.USE_FOOD,
        ord("J"): InputAction.USE_FOOD,
        ord("k"): InputAction.USE_ELIXIR,
        ord("K"): InputAction.USE_ELIXIR,
        ord("e"): InputAction.USE_SCROLL,
        ord("E"): InputAction.USE_SCROLL,
        ord("x"): InputAction.DROP,
        ord("X"): InputAction.DROP,
        10: InputAction.INTERACT,
        9: InputAction.INVENTORY,
        32: InputAction.PASS,
        27: InputAction.MENU,
    }

    MOVE_ACTIONS: dict[int, InputAction] = {
        ord("w"): InputAction.MOVE_UP,
        ord("s"): InputAction.MOVE_DOWN,
        ord("a"): InputAction.MOVE_LEFT,
        ord("d"): InputAction.MOVE_RIGHT,
        ord("W"): InputAction.MOVE_UP,
        ord("S"): InputAction.MOVE_DOWN,
        ord("A"): InputAction.MOVE_LEFT,
        ord("D"): InputAction.MOVE_RIGHT,
        curses.KEY_UP: InputAction.MOVE_UP,
        curses.KEY_DOWN: InputAction.MOVE_DOWN,
        curses.KEY_LEFT: InputAction.MOVE_LEFT,
        curses.KEY_RIGHT: InputAction.MOVE_RIGHT,
    }

    ROTATE_ACTIONS: dict[int, InputAction] = {
        ord("a"): InputAction.ROTATE_LEFT,
        ord("d"): InputAction.ROTATE_RIGHT,
        ord("A"): InputAction.ROTATE_LEFT,
        ord("D"): InputAction.ROTATE_RIGHT,
        curses.KEY_LEFT: InputAction.ROTATE_LEFT,
        curses.KEY_RIGHT: InputAction.ROTATE_RIGHT,
    }

    ACTIONS: dict[int, InputAction] = unite_dicts(BASE_ACTIONS, MOVE_ACTIONS)

    ACTIONS_3D: dict[int, InputAction] = unite_dicts(ACTIONS, ROTATE_ACTIONS)


class CursesInputHandler(InputHandler):
    @staticmethod
    def get(window: curses.window, selected_3d: bool = False) -> InputAction:
        if not isinstance(window, curses.window):
            return InputAction.UNDEFINED

        try:
            key = window.get_wch()
            CursesInputHandler.flush()
        except KeyboardInterrupt:
            return InputAction.QUIT
        except _curses.error:
            return InputAction.UNDEFINED

        actions = CursesKeymap.ACTIONS_3D if selected_3d else CursesKeymap.ACTIONS
        return actions.get(
            ord(key) if isinstance(key, str) else key, InputAction.UNDEFINED
        )

    @staticmethod
    def flush() -> None:
        curses.flushinp()
