from dataclasses import dataclass

from domain.entities.enemy import Enemy


@dataclass
class EnemyDTO:
    x: int
    y: int
    type: int
    health: float
    max_health: float
    dexterity: int
    strength: int
    level: int
    hostility: int
    home_room_index: int
    invisible: bool = False


class EnemyMaper:
    @staticmethod
    def to_dto(enemy: Enemy) -> EnemyDTO:
        return EnemyDTO(
            x=enemy.position.x,
            y=enemy.position.y,
            type=enemy.type.value,
            health=enemy.health,
            max_health=enemy.max_health,
            dexterity=enemy.dexterity,
            strength=enemy.strength,
            level=int(enemy.level),
            hostility=int(enemy.hostility),
            home_room_index=enemy.home_room_index,
            invisible=enemy.invisible,
        )
