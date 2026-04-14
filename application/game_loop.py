# TODO: Autosave, spawn, map generation, sound mixer

from application.dto.game_state import GameMapper
from config.exit import Exit
from domian.entities.game_session import GameSession
from domian.rules.progression import Level
from domian.value_objects.size import Size
from presentation.input_handler import InputAction
from presentation.window import Window


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.window: Window = window
        size = Size(*self.window.get_size())
        self.game_session: GameSession = GameSession(size)
        self.game_session.new_stage()
        self.stage: int = 0

    def run(self) -> int:
        while self.stage < len(Level):
            game_state = GameMapper.to_dto(self.game_session)
            self.window._draw(game_state)

            action: InputAction = self.window._input()

            match action:
                case InputAction.QUIT:
                    return Exit.OK
                case InputAction.MENU:
                    self.window._notify("NA", "Menu", duration=2.0)
