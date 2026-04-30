from random import random

from domain.entities.enemy import Enemy
from domain.entities.game_session import GameSession
from domain.services.combat import CombatService
from domain.services.movement import MovementService
from domain.services.pathfinding import astar
from domain.value_objects.enums import (
    EnemyAction,
    EnemyType,
    SoundType,
)
from domain.value_objects.position import Position


class EnemyAI:
    REGISTRY: dict = {}

    @staticmethod
    def action(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        ai_cls = EnemyAI.REGISTRY.get(enemy.type, EnemyAI)
        dx = abs(enemy.position.x - context.player.position.x)
        dy = abs(enemy.position.y - context.player.position.y)
        if max(dx, dy) > enemy.hostility.range:
            return ai_cls.idle(enemy, context)
        return ai_cls.act(enemy, context)

    @staticmethod
    def act(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if context.player.position.is_adjacent(enemy.position):
            enemy.path.clear()
            return EnemyAI.attack(enemy, context)
        return EnemyAI.move(enemy, context)

    @staticmethod
    def idle(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if enemy.home_room_index < 0 or enemy.home_room_index >= len(
            context.stage.rooms
        ):
            return EnemyAction.UNDEFINED
        home_room = context.stage.rooms[enemy.home_room_index]
        if not enemy.path:
            target = home_room.get_random_inbound()
            path = astar(*enemy.position, *target, context.get_obstacle_map())
            if path:
                path.pop(0)
                enemy.path = path
        if enemy.path:
            next_pos = Position(*enemy.path.pop(0))
            if home_room.is_inbound(next_pos):
                MovementService.move(enemy, next_pos, context)
        return EnemyAction.UNDEFINED

    @staticmethod
    def attack(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        hit = CombatService.hit(enemy, context.player)
        context.sounds.put(SoundType.HIT)
        if hit:
            context.statistics.hits_taken += 1
        return EnemyAction.ATTACK

    @staticmethod
    def move(enemy: "Enemy", context: "GameSession") -> EnemyAction:
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
            next_pos = Position(*enemy.path.pop(0))
            MovementService.move(enemy, next_pos, context)
        return EnemyAction.UNDEFINED


class ZombieAI(EnemyAI):
    pass


class VampireAI(EnemyAI):
    DRAIN: int = 2

    @staticmethod
    def act(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if context.player.position.is_adjacent(enemy.position):
            enemy.path.clear()
            return VampireAI.attack(enemy, context)
        return EnemyAI.move(enemy, context)

    @staticmethod
    def attack(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        hit = CombatService.hit(enemy, context.player)
        context.sounds.put(SoundType.HIT if hit else SoundType.SWING)
        if hit:
            context.statistics.hits_taken += 1
            context.player.max_health = max(
                context.player.max_health - VampireAI.DRAIN, 1
            )
            context.player.health = min(
                context.player.health, context.player.max_health
            )
        return EnemyAction.ATTACK


class GhostAI(EnemyAI):
    INVIS_CHANCE: float = 0.2

    @staticmethod
    def act(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if context.player.position.is_adjacent(enemy.position):
            enemy.invisible = False
            enemy.path.clear()
            return EnemyAI.attack(enemy, context)
        return GhostAI.move(enemy, context)

    @staticmethod
    def idle(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if not enemy.invisible and random() < GhostAI.INVIS_CHANCE:
            enemy.invisible = True
        return GhostAI.move(enemy, context)

    @staticmethod
    def move(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if enemy.home_room_index < 0 or enemy.home_room_index >= len(
            context.stage.rooms
        ):
            return EnemyAction.UNDEFINED
        home_room = context.stage.rooms[enemy.home_room_index]
        target = home_room.get_random_inbound()
        obstacle_map = context.get_obstacle_map()
        if (
            home_room.is_inbound(target)
            and not obstacle_map[target.y][target.x]
            and target != context.player.position
        ):
            enemy.position = target
            enemy.path.clear()
        return EnemyAction.MOVE


class OgreAI(EnemyAI):
    @staticmethod
    def act(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if enemy.resting:
            enemy.resting = False
            return EnemyAction.UNDEFINED
        if context.player.position.is_adjacent(enemy.position):
            enemy.path.clear()
            return OgreAI.attack(enemy, context)
        return OgreAI.move(enemy, context)

    @staticmethod
    def idle(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        OgreAI.step(enemy, context)
        OgreAI.step(enemy, context)
        return EnemyAction.UNDEFINED

    @staticmethod
    def attack(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if enemy.counter_queued:
            enemy.counter_queued = False
            damage = enemy.strength + enemy.dexterity * 0.5
            context.player.health = max(context.player.health - damage, 0)
            context.sounds.put(SoundType.HIT)
            context.statistics.hits_taken += 1
        else:
            hit = CombatService.hit(enemy, context.player)
            context.sounds.put(SoundType.HIT if hit else SoundType.SWING)
            if hit:
                context.statistics.hits_taken += 1
                enemy.resting = True
        return EnemyAction.ATTACK

    @staticmethod
    def move(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        EnemyAI.move(enemy, context)
        EnemyAI.move(enemy, context)
        return EnemyAction.UNDEFINED

    @staticmethod
    def step(enemy: "Enemy", context: "GameSession") -> None:
        if enemy.home_room_index < 0 or enemy.home_room_index >= len(
            context.stage.rooms
        ):
            return
        home_room = context.stage.rooms[enemy.home_room_index]
        if not enemy.path:
            target = home_room.get_random_inbound()
            path = astar(*enemy.position, *target, context.get_obstacle_map())
            if path:
                path.pop(0)
                enemy.path = path
        if enemy.path:
            next_pos = Position(*enemy.path.pop(0))
            if home_room.is_inbound(next_pos):
                MovementService.move(enemy, next_pos, context)


class SnakeMageAI(EnemyAI):
    SLEEP_CHANCE: float = 0.3

    @staticmethod
    def act(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if context.player.position.is_adjacent(enemy.position):
            enemy.path.clear()
            return SnakeMageAI.attack(enemy, context)
        return SnakeMageAI.move(enemy, context)

    @staticmethod
    def idle(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        return EnemyAI.idle(enemy, context)

    @staticmethod
    def attack(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        hit = CombatService.hit(enemy, context.player)
        context.sounds.put(SoundType.HIT if hit else SoundType.SWING)
        if hit:
            context.statistics.hits_taken += 1
            if random() < SnakeMageAI.SLEEP_CHANCE:
                context.player.sleep_turns = 1
        return EnemyAction.ATTACK

    @staticmethod
    def move(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if enemy.home_room_index < 0 or enemy.home_room_index >= len(
            context.stage.rooms
        ):
            return EnemyAction.UNDEFINED

        home_room = context.stage.rooms[enemy.home_room_index]
        dx, dy = enemy.diagonal_dir
        enemy.diagonal_dir = (-dx, dy)
        new_pos = Position(enemy.position.x + dx, enemy.position.y + dy)
        obstacle_map = context.get_obstacle_map()
        if (
            home_room.is_inbound(new_pos)
            and not obstacle_map[new_pos.y][new_pos.x]
            and new_pos != context.player.position
        ):
            MovementService.move(enemy, new_pos, context)
            enemy.path.clear()
            return EnemyAction.MOVE
        return EnemyAI.move(enemy, context)


EnemyAI.REGISTRY = {
    EnemyType.ZOMBIE: ZombieAI,
    EnemyType.VAMPIRE: VampireAI,
    EnemyType.GHOST: GhostAI,
    EnemyType.OGRE: OgreAI,
    EnemyType.SNAKE_MAGE: SnakeMageAI,
}
