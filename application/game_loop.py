# TODO: Autosave, spawn, map generation, sound mixer

from config.exit import Exit
from presentation.input_handler import InputAction, InputHandler
from presentation.renderer import Renderer


class GameLoop:
    def __init__(self, renderer: Renderer, input_handler: InputHandler) -> None:
        self.renderer: Renderer = renderer
        self.input_handler: InputHandler = input_handler

    def run(self) -> int:
        while True:
            # self.renderer.render()

            action: InputAction = self.input_handler.get(self.renderer.window)

            match action:
                case InputAction.QUIT:
                    return Exit.OK
                case InputAction.MOVE_UP:
                    self.renderer.notify("up", duration=2.0)
                case InputAction.MOVE_DOWN:
                    pass
