from dataclasses import dataclass
from multiprocessing import SimpleQueue
from random import choice
from typing import Optional

from domain.entities.enemy import Enemy
from domain.entities.entity import Entity
from domain.entities.item import Item
from domain.entities.player import Player
from domain.entities.stage import Stage
from domain.entities.tile import OBSTACLES, Tile
from domain.generators.enemy import EnemyFactory
from domain.generators.item import ItemFactory
from domain.generators.stage import StageFactory
from domain.generators.tiles import TileFactory
from domain.rules.progression import Level
from domain.value_objects.position import Position
from infrastructure.math import Constant
from infrastructure.vector import Size


@dataclass(eq=False)
class GameSession(Entity):
    stage: Stage
    player: Player
    enemies: list[Enemy]
    tiles: list[Tile]
    items: list[Item]
    tile_map: list[list[Tile]]
    process: bool = True
    selected_3d: bool = False

    def __init__(self, size: Size, sounds: SimpleQueue = SimpleQueue()) -> None:
        self.size: Size = size
        self.player: Player = Player(
            health=100,
            max_health=100,
            dexterity=10,
            strength=10,
            level=Level.LEVEL_1,
            position=Position(),
            rotation=Constant.PI_BY_MINUS_2,
        )
        self.cached_obstacle_map: list[list[bool]] = []
        self.sounds: SimpleQueue = sounds
        self.items = []

    def new_stage(self) -> None:
        self.stage = StageFactory.create_stage(self.size)
        self.tiles = TileFactory.get_tiles(self.stage)
        self.tile_map = TileFactory.get_tile_map(self.stage, self.tiles)
        self.get_cached_obstacle_map()
        player_room = choice(self.stage.rooms)
        self.player.position = player_room.get_random_inbound()
        if self.player.level:
            self.player.max_health = round(self.player.max_health * 1.17)
            self.player.health = self.player.max_health
            self.player.dexterity = round(self.player.dexterity * 1.1)
            self.player.strength = round(self.player.strength * 1.1)
        self.items = [item for item in self.items if item.is_owned]
        self.player.level += 1
        self.enemies = {
            EnemyFactory.create_random(room.get_random_inbound())
            for room in self.stage.rooms
            if room != player_room
        }
        for room in self.stage.rooms:
            if room != player_room:
                self.items += [
                    ItemFactory.create_random(
                        room.get_random_inbound(), self.player.level
                    ),
                    ItemFactory.create_random(
                        room.get_random_inbound(), self.player.level
                    ),
                ]

    def find_enemy(self) -> Optional[Enemy]:
        enemy_position = self.player.position + self.player.direction
        for enemy in self.enemies:
            if enemy.position == enemy_position:
                return enemy
        return None

    def get_cached_obstacle_map(self) -> list[list[bool]]:
        self.cached_obstacle_map = [
            [True] * self.size.width for _ in range(self.size.height)
        ]
        for tile in self.tiles:
            if tile.type not in OBSTACLES:
                self.cached_obstacle_map[tile.position.y][tile.position.x] = False

        return [row[:] for row in self.cached_obstacle_map]

    def get_obstacle_map(self) -> list[list[bool]]:
        # return self.cached_obstacle_map
        obstacle_map = self.get_cached_obstacle_map()

        for enemy in self.enemies:
            obstacle_map[enemy.position.y][enemy.position.x] = True

        return obstacle_map
