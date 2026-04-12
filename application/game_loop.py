# TODO: Autosave, spawn, map generation, sound mixer

from config.exit import Exit
from presentation.input_handler import InputAction
from presentation.window import Window


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.window: Window = window

    def run(self) -> int:
        while True:
            # self.window._draw()

            action: InputAction = self.window._input()

            match action:
                case InputAction.QUIT:
                    return Exit.OK
                case InputAction.MENU:
                    self.window._notify("NA", "Menu", duration=2.0)
