from dataclasses import dataclass

from domian.entities.enemy import Enemy
from domian.value_objects.enums import EnemyType


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
