# TODO: Autosave, fog of war, items, backpack, stairs
from application.commands.assembler import CommandAssembler
from application.commands.command import CommandResult, CommandService
from application.dto.game_state import GameMapper
from application.sounds.assembler import SoundAssembler
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
        self.window: Window = window
        # size = Size(*self.window.get_size()) / 3 for 3d
        size = Size(*self.window.get_size())
        self.game_session: GameSession = GameSession(size)
        self.game_session.new_stage()
        self.stage: int = 0
        self.mixer = Mixer()

    def run(self) -> None:
        self.mixer.start()
        CommandAssembler.assemble_commands()
        SoundAssembler.assemble_sounds(self.mixer)
        # SpriteAssembler.assemble_sprites()
        self.game_session.sounds.append(SoundType.MUSIC)
        self.mixer.play(self.game_session)
        # self.game_session.selected_3d = True
        while self.game_session.process:
            game_state = GameMapper.to_dto(self.game_session)

            self.window.draw(game_state)

            action: InputAction = self.window.action()
            result = CommandService(action, self.game_session, self.window).execute()
            if result == CommandResult.NO_ACTION:
                continue

            for enemy in self.game_session.enemies:
                EnemyAI.action(enemy, self.game_session)

            if self.game_session.player.health <= 0:
                self.game_session.sounds.append(SoundType.DEATH)
                self.game_session.process = False

            self.mixer.play(self.game_session)

        if self.stage < len(Level):
            self.window.draw(GameMapper.to_dto(self.game_session))
            self.window.game_over()
