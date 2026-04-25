from math import cos, sin

from application.commands.command import Command, CommandResult
from domain.entities.game_session import GameSession
from domain.services.combat import CombatService
from domain.services.movement import MovementService
from domain.value_objects.enums import SoundType
from domain.value_objects.position import Direction, Position


class Move(Command):
    def __init__(self, direction: Direction) -> None:
        self.direction = direction

    def execute(self, context: GameSession, *args, **kwargs) -> CommandResult:
        if context.selected_3d:
            rot = context.player.rotation
            sin_r, cos_r = round(sin(rot)), round(cos(rot))
            match self.direction:
                case Direction.UP:
                    d = Position(cos_r, sin_r)
                case Direction.DOWN:
                    d = Position(-cos_r, -sin_r)
                case Direction.LEFT:
                    d = Position(sin_r, -cos_r)
                case Direction.RIGHT:
                    d = Position(-sin_r, cos_r)
            new_position = context.player.position + d
            context.player.direction = d
        else:
            new_position = context.player.position + self.direction
            context.player.direction = self.direction
        if not MovementService.move(context.player, new_position, context):
            if CombatService.attack(context):
                context.sounds.put(SoundType.SWING)
                return CommandResult.SWAP_ACTION
            return CommandResult.NO_ACTION
        context.sounds.put(SoundType.MOVE)
        return CommandResult.OK
