from typing import Optional

from application.commands.command import Command
from domain.entities.game_session import GameSession
from domain.services.movement import MovementService
from domain.value_objects.enums import SoundType
from domain.value_objects.position import Direction


class Move(Command):
    def __init__(self, direction: Optional[Direction] = None) -> None:
        self.direction = direction

    def execute(self, session: GameSession, *args, **kwargs):
        new_position = session.player.position + self.direction
        session.player.direction = self.direction
        if not MovementService.move(session.player, new_position, session):
            return
        session.sounds.append(SoundType.MOVE)
