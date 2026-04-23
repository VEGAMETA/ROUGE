import _curses
import curses

from presentation.input_handler import InputAction, InputHandler


class CursesKeymap:
    ACTIONS: dict[int, InputAction] = {
        ord("q"): InputAction.QUIT,
        ord("w"): InputAction.MOVE_UP,
        ord("s"): InputAction.MOVE_DOWN,
        ord("a"): InputAction.MOVE_LEFT,
        ord("d"): InputAction.MOVE_RIGHT,
        ord("j"): InputAction.ROTATE_LEFT,
        ord("k"): InputAction.ROTATE_RIGHT,
        curses.KEY_UP: InputAction.MOVE_UP,
        curses.KEY_DOWN: InputAction.MOVE_DOWN,
        curses.KEY_LEFT: InputAction.MOVE_LEFT,
        curses.KEY_RIGHT: InputAction.MOVE_RIGHT,
        32: InputAction.PASS,
        ord("e"): InputAction.INTERACT,
        curses.KEY_ENTER: InputAction.INTERACT,
        9: InputAction.INVENTORY,
        27: InputAction.MENU,
    }


class CursesInputHandler(InputHandler):
    @staticmethod
    def get(window: curses.window) -> InputAction:
        if not isinstance(window, curses.window):
            return InputAction.UNDEFINED

        try:
            key = window.get_wch()
            CursesInputHandler.flush()
        except KeyboardInterrupt:
            return InputAction.QUIT
        except _curses.error:
            return InputAction.UNDEFINED

        return CursesKeymap.ACTIONS.get(
            ord(key) if isinstance(key, str) else key, InputAction.UNDEFINED
        )

    @staticmethod
    def flush() -> None:
        curses.flushinp()
