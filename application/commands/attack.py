from application.commands.command import Command
from domain.entities.game_session import GameSession
from domain.services.combat import CombatService
from domain.value_objects.enums import SoundType


class Attack(Command):
    def execute(self, context: GameSession, *args, **kwargs) -> None:
        if CombatService.attack(context):
            context.sounds.append(SoundType.SWING)
