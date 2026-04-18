from dataclasses import dataclass
from random import choice
from typing import Optional

from domain.entities.enemy import Enemy
from domain.entities.entity import Entity
from domain.entities.item import Item
from domain.entities.player import Player
from domain.entities.stage import Stage
from domain.entities.tile import OBSTACLES, Tile
from domain.generators.enemy import EnemyFactory
from domain.generators.stage import StageFactory
from domain.generators.tiles import TileFactory
from domain.rules.progression import Level
from domain.value_objects.enums import SoundType
from domain.value_objects.position import Position
from domain.value_objects.rotation import Rotation
from domain.value_objects.size import Size


@dataclass(eq=False)
class GameSession(Entity):
    stage: Stage
    player: Player
    enemies: list[Enemy]
    tiles: list[Tile]
    items: list[Item]
    sounds: list[SoundType]
    tile_map: list[list[Tile]]
    process: bool = True
    player_turn: bool = True

    def __init__(self, size: Size) -> None:
        self.size: Size = size
        self.player: Player = Player(
            health=1,
            max_health=1,
            dexterity=1,
            strength=1,
            level=Level.LEVEL_1,
            position=Position(),
            rotation=Rotation(),
        )

    def new_stage(self) -> None:
        self.stage = StageFactory.create_stage(self.size)
        self.tiles = TileFactory.get_tiles(self.stage)
        self.tile_map = TileFactory.get_tile_map(self.stage, self.tiles)
        player_room = choice(self.stage.rooms)
        self.player.position = player_room.get_random_inbound()
        self.enemies = {
            EnemyFactory.create_random(room.get_random_inbound())
            for room in self.stage.rooms
            if room != player_room
        }
        self.items = []
        self.sounds = []

    def find_enemy(self) -> Optional[Enemy]:
        enemy_position = self.player.position + self.player.direction
        for enemy in self.enemies:
            if enemy.position == enemy_position:
                return enemy
        return None

    def get_obstacle_map(self) -> list[list[bool]]:
        obstacle_map = [[True] * self.size.width for _ in range(self.size.height)]
        for tile in self.tiles:
            if tile.type not in OBSTACLES:
                obstacle_map[tile.position.y][tile.position.x] = False
        for enemy in self.enemies:
            obstacle_map[enemy.position.y][enemy.position.x] = True
        return obstacle_map
