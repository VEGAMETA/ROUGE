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
            if self.direction == Direction.UP:
                x = int(round(cos(context.player.rotation)))
                y = int(round(sin(context.player.rotation)))
                new_position = Position(
                    context.player.position.x + x, context.player.position.y + y
                )
            if self.direction == Direction.DOWN:
                x = int(round(cos(context.player.rotation)))
                y = int(round(sin(context.player.rotation)))
                new_position = Position(
                    context.player.position.x - x, context.player.position.y - y
                )
            if self.direction == Direction.LEFT:
                x = int(round(sin(context.player.rotation)))
                y = int(round(cos(context.player.rotation)))
                new_position = Position(
                    context.player.position.x + x, context.player.position.y - y
                )
            if self.direction == Direction.RIGHT:
                x = int(round(sin(context.player.rotation)))
                y = int(round(cos(context.player.rotation)))
                new_position = Position(
                    context.player.position.x - x, context.player.position.y + y
                )
            context.player.direction = Position(x, y)
        else:
            new_position = context.player.position + self.direction
            context.player.direction = self.direction
        if not MovementService.move(context.player, new_position, context):
            if CombatService.attack(context):
                context.sounds.append(SoundType.SWING)
                return CommandResult.SWAP_ACTION
            return CommandResult.NO_ACTION
        context.sounds.append(SoundType.MOVE)
        return CommandResult.OK
