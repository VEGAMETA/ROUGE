from application.commands.attack import Attack
from application.commands.command import CommandService
from application.commands.idle import Idle
from application.commands.inventory import Inventory
from application.commands.menu import Menu
from application.commands.move import Move
from application.commands.quit import Quit
from domain.value_objects.position import Direction
from presentation.input_handler import InputAction


class CommandAssembler:
    @staticmethod
    def assemble_commands():
        CommandService.register(InputAction.UNDEFINED, lambda: Idle())
        CommandService.register(InputAction.QUIT, lambda: Quit())
        CommandService.register(InputAction.ATTACK, lambda: Attack())
        CommandService.register(InputAction.MOVE_UP, lambda: Move(Direction.UP))
        CommandService.register(InputAction.MOVE_DOWN, lambda: Move(Direction.DOWN))
        CommandService.register(InputAction.MOVE_LEFT, lambda: Move(Direction.LEFT))
        CommandService.register(InputAction.MOVE_RIGHT, lambda: Move(Direction.RIGHT))
        CommandService.register(InputAction.MENU, lambda: Menu())
        CommandService.register(InputAction.INVENTORY, lambda: Inventory())
