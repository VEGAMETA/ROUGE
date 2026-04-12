from application.commands.command import Command
from domian.entities.enemy import Enemy
from domian.entities.player import Player
from domian.services.combat import CombatService


class Attack(Command):
    @staticmethod
    def execute(player: Player, target: Enemy):
        CombatService.attack(player, target)
