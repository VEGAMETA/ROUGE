from typing import overload
from functools import singledispatch
from domian.entities.enemy import Enemy
from domian.entities.player import Player
from domian.value_objects.position import Position


class MovementService:
    @staticmethod
    def move(entity, position: Position) -> None:
        if isinstance(entity, Player):
            entity.position += position
        elif isinstance(entity, Enemy):
            entity.position += entity.ai.next_direction()
