from dataclasses import dataclass

from domian.entities.enemy import Enemy
from domian.entities.item import Item
from domian.entities.player import Player
from domian.entities.stage import Stage
from domian.entities.tile import Tile
from domian.generators.stage import StageFactory
from domian.generators.tiles import TileFactory
from domian.value_objects.position import Position
from domian.value_objects.rotation import Rotation
from domian.value_objects.size import Size


@dataclass
class GameSession:
    stage: Stage
    player: Player
    enemies: list[Enemy]
    tiles: list[Tile]
    items: list[Item]

    def __init__(self, size: Size) -> None:
        self.size: Size = size
        self.player: Player = Player(Position(), Rotation())

    def new_stage(self):
        self.stage = StageFactory.create_stage(self.size)
        self.tiles = TileFactory.get_tiles(self.stage)
        self.enemies = []
        self.items = []
