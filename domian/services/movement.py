from typing import overload

from domian.entities.enemy import Enemy
from domian.entities.player import Player
from domian.value_objects.position import Direction


class MovementService:
    @overload
    def move(self, player: Player, direction: Direction) -> None:
        player.position += direction

    @overload
    def move(self, enemy: Enemy) -> None:
        enemy.position += enemy.ai.next_direction()
