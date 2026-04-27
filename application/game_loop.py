# TODO: Autosave, fog of war, stairs, menu, leaderboard, death/win screen
import time
from multiprocessing import SimpleQueue

from application.commands.assembler import CommandAssembler
from application.commands.command import CommandResult, CommandService
from application.dto.game_state import GameMapper, GameStateDTO
from domain.entities.game_session import GameSession
from domain.rules.progression import Level
from domain.services.ai import EnemyAI
from domain.value_objects.enums import SoundType
from infrastructure.audio.mixer import Mixer
from infrastructure.vector import Size
from presentation.input_handler import InputAction
from presentation.window import Window


class GameLoop:
    def __init__(self, window: Window, selected_3d: bool = False) -> None:
        self.window: Window = window(selected_3d)
        size: Size = Size(*self.window.get_size())
        if selected_3d:
            size /= 3
        self.stage: int = 0
        self.game_session: GameSession = GameSession(size, SimpleQueue())
        self.game_session.selected_3d = selected_3d
        self.game_session.new_stage()
        self.mixer: Mixer = Mixer(self.game_session.sounds)
        self.mixer.start()

    def run(self) -> None:
        CommandAssembler.assemble_commands()
        self.game_session.sounds.put(SoundType.MUSIC)
        game_timer: float = time.monotonic()
        tick_timer: float = time.perf_counter()
        tick_t: float = 0
        while self.game_session.process:
            tick_timer = time.perf_counter()

            game_state: GameStateDTO = GameMapper.to_dto(self.game_session)

            self.window.draw(game_state, tick_t)  # 0.004 s

            action: InputAction = self.window.action(self.game_session.selected_3d)

            result: CommandResult = CommandService.execute(
                action, self.game_session, self.window
            )
            if result == CommandResult.NO_ACTION:
                tick_t = time.perf_counter() - tick_timer
                continue

            for enemy in self.game_session.enemies:  # 0.00-0.01 s
                EnemyAI.action(enemy, self.game_session)

            if self.game_session.player.health <= 0:
                self.game_session.sounds.put(SoundType.DEATH)
                self.game_session.process = False
            if self.game_session.player.position == self.game_session.stairs.position:
                self.game_session.sounds.put(SoundType.LEVEL_UP)
                self.game_session.new_stage()
            tick_t = time.perf_counter() - tick_timer

        self.mixer.join(0.1)
        if self.game_session.player.health <= 0 and self.stage < len(Level):
            self.window.draw(GameMapper.to_dto(self.game_session), tick_t)
            self.window.game_over(time.monotonic() - game_timer)
