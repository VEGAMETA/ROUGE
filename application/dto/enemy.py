from dataclasses import dataclass

from domain.entities.enemy import Enemy
from domain.value_objects.enums import EnemyType


@dataclass
class EnemyDTO:
    x: int
    y: int
    type: EnemyType


class EnemyMaper:
    @staticmethod
    def to_dto(enemy: Enemy):
        return EnemyDTO(
            x=enemy.position.x,
            y=enemy.position.y,
            type=enemy.type,
        )
