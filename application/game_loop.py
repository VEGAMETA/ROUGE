# TODO: Autosave, fog of war, death/win screen
import getpass
import time
from datetime import datetime
from multiprocessing import SimpleQueue

from application.commands.assembler import CommandAssembler
from application.commands.command import CommandResult, CommandService
from application.dto.game_save import GameSaveMapper
from application.dto.game_state import GameMapper, GameStateDTO
from domain.entities.game_session import GameSession
from domain.rules.progression import Level
from domain.services.ai import EnemyAI
from domain.services.visibility import Visibility
from domain.value_objects.enums import SoundType
from infrastructure.audio.mixer import Mixer
from infrastructure.persistence.leaderboard import Leaderboard, LeaderboardRecord
from infrastructure.vector import Size
from presentation.input_handler import InputAction
from presentation.window import Window


class GameLoop:
    def __init__(self, window: Window, selected_3d: bool = False) -> None:
        self.selected_3d: bool = selected_3d
        self.window: Window = window(selected_3d)
        self.size: Size = Size(*self.window.get_size())
        if selected_3d:
            self.size /= 3
        self.stage: int = 0
        self.game_session: GameSession = GameSession(self.size, SimpleQueue())
        self.game_session.selected_3d = selected_3d
        self.game_session.new_stage()
        self.mixer: Mixer = Mixer(self.game_session.sounds)
        self.mixer.start()

    @staticmethod
    def build_record(session: GameSession, name: str) -> LeaderboardRecord:
        s = session.statistics
        return LeaderboardRecord(
            name=name,
            treasure=session.points,
            level=s.level_reached,
            enemies=s.enemies_defeated,
            food=s.food_consumed,
            elixirs=s.elixirs_used,
            scrolls=s.scrolls_read,
            attacks=s.attacks_made,
            hits=s.hits_taken,
            tiles=s.tiles_traversed,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )

    def run(self) -> bool:
        CommandAssembler.assemble_commands()
        self.game_session.sounds.put(SoundType.MUSIC)
        game_timer: float = time.monotonic()
        tick_timer: float = time.perf_counter()
        tick_t: float = 0
        if GameSaveMapper.file_exists():
            CommandService.execute(InputAction.MENU, self.game_session, self.window)
        while self.game_session.process:
            tick_timer = time.perf_counter()
            if self.game_session.player.sleep_turns > 0:
                self.game_session.player.sleep_turns -= 1
                for enemy in self.game_session.enemies:
                    EnemyAI.action(enemy, self.game_session)
                Visibility.update(self.game_session)
                if self.game_session.player.health <= 0:
                    self.game_session.sounds.put(SoundType.DEATH)
                    Leaderboard.append(
                        GameLoop.build_record(self.game_session, getpass.getuser())
                    )
                    self.game_session.process = False
                tick_t = time.perf_counter() - tick_timer
                continue
            Visibility.update(self.game_session)
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
                Leaderboard.append(
                    GameLoop.build_record(self.game_session, getpass.getuser())
                )
                self.game_session.process = False
            tick_t = time.perf_counter() - tick_timer

        self.mixer.q.put(SoundType.STOP)
        self.mixer.join(0.1)

        elapsed = time.monotonic() - game_timer
        if self.game_session.player.health <= 0 and self.stage < len(Level):
            self.window.draw(GameMapper.to_dto(self.game_session), tick_t)
            self.window.game_over(
                elapsed, self.game_session.statistics, self.game_session.points
            )
            return False
        if int(self.game_session.player.level) > len(Level):
            Leaderboard.append(
                GameLoop.build_record(self.game_session, getpass.getuser())
            )
            self.window.draw(GameMapper.to_dto(self.game_session), tick_t)
            self.window.victory(
                elapsed, self.game_session.statistics, self.game_session.points
            )
        return True
