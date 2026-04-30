from math import cos, sin

from application.commands.command import Command, CommandResult
from domain.entities.game_session import GameSession
from domain.services.combat import CombatService
from domain.services.item import ItemService
from domain.services.movement import MovementService
from domain.value_objects.enums import DoorType, SoundType
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
        for door in context.doors:
            if door.type == DoorType.OPENED:
                continue
            if door.position != new_position:
                continue
            if door.type not in map(lambda x: x.type, context.owned_keys):
                return CommandResult.NO_ACTION
            context.sounds.put(SoundType.DOOR)
        if not MovementService.move(context.player, new_position, context):
            if CombatService.attack(context):
                return CommandResult.SWAP_ACTION
            return CommandResult.NO_ACTION
        context.sounds.put(SoundType.MOVE)
        for item in context.items:
            if not item.is_owned and context.player.position == item.position:
                if ItemService.pickup(item, context):
                    context.sounds.put(SoundType.ITEM_PICK)
                break
        for key in context.keys:
            if (
                key not in context.owned_keys
                and context.player.position == key.position
            ):
                if ItemService.pickup_key(key, context):
                    context.sounds.put(SoundType.ITEM_PICK)
                break
        if context.player.position == context.stairs.position:
            context.sounds.put(SoundType.LEVEL_UP)
            context.new_stage()
        return CommandResult.OK
