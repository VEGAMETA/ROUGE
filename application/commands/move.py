from typing import Optional

from application.commands.command import Command
from domain.entities.game_session import GameSession
from domain.services.movement import MovementService
from domain.value_objects.position import Direction


class Move(Command):
    def __init__(self, direction: Optional[Direction] = None) -> None:
        self.direction = direction

    def execute(self, session: GameSession, *args, **kwargs):
        MovementService.move(session, self.direction)
