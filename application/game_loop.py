# TODO: Autosave, fog of war, items, backpack, stairs
import time
from multiprocessing import SimpleQueue
from queue import Empty

from application.commands.assembler import CommandAssembler
from application.commands.command import CommandResult, CommandService
from application.dto.game_state import GameMapper, GameStateDTO
from config.settings import TARGET_FPS
from domain.entities.game_session import GameSession
from domain.rules.progression import Level
from domain.services.ai import EnemyAI
from domain.value_objects.enums import SoundType
from domain.value_objects.size import Size
from infrastructure.audio.mixer import Mixer
from presentation.curses.sprites import SpriteAssembler
from presentation.input_handler import InputAction
from presentation.window import Window


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.window: Window = window()
        size = Size(*self.window.get_size())
        size /= 3  # 3D
        self.stage: int = 0
        self.game_session: GameSession = GameSession(size, SimpleQueue())
        self.game_session.selected_3d = True  # 3D
        self.game_session.new_stage()
        self.mixer = Mixer(self.game_session.sounds)
        self.mixer.start()

    def run(self) -> None:
        CommandAssembler.assemble_commands()
        SpriteAssembler.assemble_sprites()
        self.game_session.sounds.put(SoundType.MUSIC)
        self.game_session.selected_3d = False
        game_timer = time.monotonic()
        tick_timer = time.perf_counter()
        tick_t = 0
        while self.game_session.process:
            tick_timer = time.perf_counter()

            game_state: GameStateDTO = GameMapper.to_dto(self.game_session)

            self.window.draw(game_state)  # 0.004 s

            self.window.renderer.window.addstr(0, 0, f"{tick_t:.4f}s")
            self.window.renderer.window.refresh()

            action: InputAction = self.window.action()

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
            tick_t = time.perf_counter() - tick_timer

        self.mixer.join(0.1)
        if self.stage < len(Level):
            self.window.draw(GameMapper.to_dto(self.game_session))
            self.window.game_over(time.monotonic() - game_timer)
