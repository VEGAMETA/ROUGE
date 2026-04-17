# TODO: Autosave, spawn, map generation, sound mixer
from application.commands.assembler import CommandAssembler
from application.commands.command import CommandService
from application.dto.game_state import GameMapper
from domain.entities.game_session import GameSession
from domain.rules.progression import Level
from domain.services.ai import EnemyAI
from domain.value_objects.size import Size
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
        CommandAssembler.assemble_commands()
        while self.stage < len(Level) and self.game_session.process:
            game_state = GameMapper.to_dto(self.game_session)
            self.window.draw(game_state)
            action: InputAction = self.window.action()
            self.game_session.player_turn = True
            CommandService(action, self.game_session, self.window).execute()
            self.game_session.player_turn = False
            for enemy in self.game_session.enemies:
                EnemyAI.action(enemy, self.game_session)
