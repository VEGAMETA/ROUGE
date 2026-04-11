from dataclasses import dataclass

from domian.entities.enemy import Enemy
from domian.entities.item import Item
from domian.entities.player import Player
from domian.entities.tile import Tile


@dataclass
class GameSession:
    player: Player
    enemies: list[Enemy]
    tiles: list[Tile]
    items: list[Item]
