from dataclasses import dataclass

from domain.entities.player import Player


@dataclass
class PlayerDTO:
    x: int
    y: int
    health: int
    max_health: int
    dexterity: int
    strength: int
    level: int
    rotation: float
    weapon_name: str = ""


class PlayerMapper:
    @staticmethod
    def to_dto(player: Player):
        return PlayerDTO(
            x=player.position.x,
            y=player.position.y,
            health=player.health,
            max_health=player.max_health,
            dexterity=player.dexterity,
            strength=player.strength,
            level=player.level,
            rotation=player.rotation,
            weapon_name=player.weapon.name if player.weapon else "",
        )
