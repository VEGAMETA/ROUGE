from application.commands.command import Command, CommandResult
from application.dto.game_save import GameSaveMapper
from domain.entities.game_session import GameSession
from infrastructure.persistence.leaderboard import Leaderboard
from presentation.views.menu import MenuAction
from presentation.window import Window


class Menu(Command):
    def execute(
        self, context: GameSession, window: Window, *args, **kwargs
    ) -> CommandResult:
        action = window.show_menu()
        if action == MenuAction.EXIT:
            context.process = False
            return CommandResult.QUIT
        if action == MenuAction.LEADERBOARD:
            window.show_leaderboard(Leaderboard.read())
        if action == MenuAction.SAVE:
            GameSaveMapper.save(context)
            window.notify("Game saved", "Save", duration=2.0)
        if action == MenuAction.LOAD:
            if GameSaveMapper.file_exists():
                GameSaveMapper.load(context)
            else:
                window.notify("No save found", "Load", duration=2.0)
        return CommandResult.NO_ACTION
