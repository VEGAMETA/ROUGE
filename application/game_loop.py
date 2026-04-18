# TODO: Autosave, spawn, map generation, sound mixer
from application.commands.assembler import CommandAssembler
from application.commands.command import CommandService
from application.dto.game_state import GameMapper
from application.sounds.assembler import SoundAssembler
from domain.entities.game_session import GameSession
from domain.rules.progression import Level
from domain.services.ai import EnemyAI
from domain.value_objects.enums import SoundType
from domain.value_objects.size import Size
from infrastructure.audio.mixer import Mixer
from presentation.input_handler import InputAction
from presentation.window import Window


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.window: Window = window
        size = Size(*self.window.get_size())
        self.game_session: GameSession = GameSession(size)
        self.game_session.new_stage()
        self.stage: int = 0
        self.mixer = Mixer()

    def run(self) -> None:
        self.mixer.start()
        CommandAssembler.assemble_commands()
        SoundAssembler.assemble_sounds(self.mixer)
        self.game_session.sounds.append(SoundType.MUSIC)

        while self.game_session.process:
            game_state = GameMapper.to_dto(self.game_session)
            self.window.draw(game_state)
            action: InputAction = self.window.action()
            CommandService(action, self.game_session, self.window).execute()
            for enemy in self.game_session.enemies:
                EnemyAI.action(enemy, self.game_session)
            if self.game_session.player.health <= 0:
                self.game_session.sounds.append(SoundType.DEATH)
                self.game_session.process = False
            self.mixer.play(self.game_session)

        if self.stage < len(Level):
            self.window.game_over()
