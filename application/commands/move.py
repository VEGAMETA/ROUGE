from application.commands.command import Command
from domian.entities.player import Player
from domian.services.movement import MovementService
from domian.value_objects.position import Direction


class Move(Command):
    @staticmethod
    def execute(player: Player, direction: Direction):
        MovementService.move(player, direction)
