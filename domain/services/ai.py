from domain.entities.enemy import Enemy
from domain.entities.game_session import GameSession
from domain.services.combat import CombatService
from domain.services.movement import MovementService
from domain.services.pathfinding import astar
from domain.value_objects.enums import EnemyAction


class EnemyAI:
    @staticmethod
    def action(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if context.player_turn:
            return EnemyAction.UNDEFINED
        if context.player.position.is_adjacent(enemy.position):
            return EnemyAI.attack(enemy, context)
        return EnemyAI.move(enemy, context)

    @staticmethod
    def attack(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        CombatService.hit(enemy, context.player)
        return EnemyAction.ATTACK

    @staticmethod
    def move(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if (
            path := astar(
                *enemy.position,
                *context.player.position,
                context.get_obstacle_map(),
            )
            is None
        ):
            return EnemyAction.UNDEFINED

        if path and len(path):
            MovementService.move_ai(enemy, path[1], context)
        return EnemyAction.UNDEFINED


class ZombieAI(EnemyAI): ...


class VampireAI(EnemyAI): ...


class GhostAI(EnemyAI): ...


class OgreAI(EnemyAI): ...


class SnakeMageAI(EnemyAI): ...
