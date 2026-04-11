from presentation.curses.renderer import CursesRenderer2D
from presentation.input_handler import InputAction, InputHandler


class CursesInputHandler(InputHandler):
    def __init__(self, renderer: CursesRenderer2D) -> None:
        super().__init__(renderer)
        self.window = renderer.window

    def get(self) -> InputAction:
        key = self.window.getkey()
        match key:
            case "q":
                return InputAction.QUIT
            case "w":
                return InputAction.MOVE_UP
            case "s":
                return InputAction.MOVE_DOWN
            case "a":
                return InputAction.MOVE_LEFT
            case "d":
                return InputAction.MOVE_RIGHT
            case "e":
                return InputAction.ATTACK
            case "m":
                return InputAction.MENU
            case "i":
                return InputAction.INVENTORY
            case "r":
                return InputAction.INTERRACT
            case "p":
                return InputAction.PICKUP
            case "o":
                return InputAction.DROP
            case _:
                return InputAction.UNDEFINED
