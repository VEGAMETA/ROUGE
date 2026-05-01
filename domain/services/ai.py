from random import choice, random

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
        if enemy.type == EnemyType.MIMIC1:
            return EnemyAction.UNDEFINED
        # home_room = context.stage.rooms[enemy.home_room_index]
        ai_cls: EnemyAI = EnemyAI.REGISTRY.get(enemy.type, EnemyAI)
        enemy.chasing = (
            context.player.position - enemy.position
        ).length() <= enemy.hostility
        if not enemy.chasing:
            return ai_cls.idle(enemy, context)
        enemy.path.clear()
        return ai_cls.act(enemy, context)

    @staticmethod
    def act(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        ai_cls = EnemyAI.REGISTRY.get(enemy.type, EnemyAI)
        if context.player.position.is_adjacent(enemy.position):
            enemy.path.clear()
            return ai_cls.attack(enemy, context)
        return ai_cls.move(enemy, context)

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
        context.sounds.put_nowait(SoundType.HIT)
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
            if next_pos == context.player.position:
                enemy.path.clear()
                return EnemyAction.UNDEFINED
            MovementService.move(enemy, next_pos, context)
        return EnemyAction.UNDEFINED


class ZombieAI(EnemyAI):
    pass


class MimicAI(EnemyAI):
    pass


class VampireAI(EnemyAI):
    DRAIN: int = 2

    @staticmethod
    def attack(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        hit = CombatService.hit(enemy, context.player)
        context.sounds.put_nowait(SoundType.HIT if hit else SoundType.SWING)
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
        EnemyAI.act(enemy, context)

    @staticmethod
    def idle(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if not enemy.invisible and random() < GhostAI.INVIS_CHANCE:
            enemy.invisible = True
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
        EnemyAI.act(enemy, context)

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
            context.sounds.put_nowait(SoundType.HIT)
            context.statistics.hits_taken += 1
        else:
            hit = CombatService.hit(enemy, context.player)
            context.sounds.put_nowait(SoundType.HIT if hit else SoundType.SWING)
            if hit:
                context.statistics.hits_taken += 1
                enemy.resting = True
        return EnemyAction.ATTACK

    @staticmethod
    def move(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        EnemyAI.move(enemy, context)
        return EnemyAI.move(enemy, context)

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
    DIAGONAL_DIRECTIONS: list[tuple[int, int]] = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    @staticmethod
    def idle(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        if enemy.home_room_index < 0 or enemy.home_room_index >= len(
            context.stage.rooms
        ):
            return EnemyAction.UNDEFINED

        home_room = context.stage.rooms[enemy.home_room_index]
        directions = SnakeMageAI.DIAGONAL_DIRECTIONS
        dx, dy = choice(directions)
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

    @staticmethod
    def attack(enemy: "Enemy", context: "GameSession") -> EnemyAction:
        hit = CombatService.hit(enemy, context.player)
        context.sounds.put_nowait(SoundType.HIT if hit else SoundType.SWING)
        if hit:
            context.statistics.hits_taken += 1
            if random() < SnakeMageAI.SLEEP_CHANCE:
                context.player.sleep_turns = 1
        return EnemyAction.ATTACK


EnemyAI.REGISTRY = {
    EnemyType.ZOMBIE: ZombieAI,
    EnemyType.VAMPIRE: VampireAI,
    EnemyType.GHOST: GhostAI,
    EnemyType.OGRE: OgreAI,
    EnemyType.SNAKE_MAGE: SnakeMageAI,
    EnemyType.MIMIC2: MimicAI,
}
