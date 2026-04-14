from config.exit import Exit
from domian.entities.game_session import GameSession
from domian.services.combat import CombatService
from domian.services.movement import MovementService
from domian.value_objects.position import Direction
from presentation.input_handler import InputAction
from presentation.window import Window


class CommandService:
    def __init__(self, action: InputAction, session: GameSession, window: Window) -> None:
        self.action: InputAction = action
        self.session: GameSession = session
        self.window: Window = window
        self.execute()

    def execute(self) -> Exit:

        match self.action:
            case InputAction.QUIT:
                self.session.process = False
            case InputAction.MENU:
                self.window._notify("NA", "Menu", duration=2.0)
            case InputAction.MOVE_UP:
                MovementService.move(self.session.player, self.session, Direction.UP)
            case InputAction.MOVE_DOWN:
                MovementService.move(self.session.player, self.session, Direction.DOWN)
            case InputAction.MOVE_LEFT:
                MovementService.move(self.session.player, self.session, Direction.LEFT)
            case InputAction.MOVE_RIGHT:
                MovementService.move(self.session.player, self.session, Direction.RIGHT)
            case InputAction.ATTACK:
                CombatService

        return Exit.OK
