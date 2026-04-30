from dataclasses import dataclass

from domain.entities.enemy import Enemy


@dataclass
class EnemyDTO:
    x: int
    y: int
    type: int
    health: int


class EnemyMaper:
    @staticmethod
    def to_dto(enemy: Enemy):
        return EnemyDTO(
            x=enemy.position.x,
            y=enemy.position.y,
            type=enemy.type.value,
            health=enemy.health,
        )
