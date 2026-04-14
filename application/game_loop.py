# TODO: Autosave, spawn, map generation, sound mixer
from application.commands.service import CommandService
from application.dto.game_state import GameMapper
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

    def run(self) -> None:
        while self.stage < len(Level) and self.game_session.process:
            game_state = GameMapper.to_dto(self.game_session)
            self.window._draw(game_state)

            action: InputAction = self.window._input()

            CommandService(action, self.game_session, self.window)
