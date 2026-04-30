from domain.entities.enemy import Enemy
from domain.entities.game_session import GameSession
from domain.services.combat import CombatService
from domain.services.movement import MovementService
from domain.services.pathfinding import astar
from domain.value_objects.enums import EnemyAction, SoundType
from domain.value_objects.position import Position


class EnemyAI:
    @staticmethod
    def action(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if context.player.position.is_adjacent(enemy.position):
            enemy.path.clear()
            return EnemyAI.attack(enemy, context)
        return EnemyAI.move(enemy, context)

    @staticmethod
    def attack(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if CombatService.hit(enemy, context.player):
            context.dds -= 0.04
        context.sounds.put(SoundType.HIT)
        return EnemyAction.ATTACK

    @staticmethod
    def move(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if (context.player.position - enemy.position).length() <= enemy.hostility:
            return EnemyAI.move_to_player(enemy, context) == EnemyAction.UNDEFINED

    @staticmethod
    def move_to_player(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if not enemy.path:
            path: list[tuple[int, int]] | None = astar(
                *enemy.position,
                *context.player.position,
                context.get_obstacle_map(),
            )
            if not path:
                return EnemyAction.UNDEFINED
            path.pop(0)
            enemy.path = path
        if enemy.path:
            MovementService.move(enemy, Position(*enemy.path.pop(0)), context)
        return EnemyAction.UNDEFINED


class ZombieAI(EnemyAI): ...


class VampireAI(EnemyAI): ...


class GhostAI(EnemyAI): ...


class OgreAI(EnemyAI): ...


class SnakeMageAI(EnemyAI): ...
