from application.commands.command import Command, CommandResult
from domain.entities.game_session import GameSession
from domain.services.combat import CombatService
from domain.services.movement import MovementService
from domain.value_objects.enums import SoundType
from domain.value_objects.position import Direction


class Move(Command):
    def __init__(self, direction: Direction) -> None:
        self.direction = direction

    def execute(self, context: GameSession, *args, **kwargs) -> CommandResult:
        new_position = context.player.position + self.direction
        context.player.direction = self.direction
        if not MovementService.move(context.player, new_position, context):
            if CombatService.attack(context):
                context.sounds.append(SoundType.SWING)
                return CommandResult.SWAP_ACTION
            return CommandResult.NO_ACTION
        context.sounds.append(SoundType.MOVE)
        return CommandResult.OK
