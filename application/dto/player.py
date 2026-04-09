from dataclasses import dataclass

from domian.entities.player import Player


@dataclass
class PlayerDTO:
    x: int
    y: int
    health: int
    max_health: int
    dextrisity: int
    strength: int
    level: int


class PlayerMapper:
    @staticmethod
    def to_dto(player: Player):
        return PlayerDTO(
            x=player.position.x,
            y=player.position.y,
            health=player.health,
            max_health=player.max_health,
            dextrisity=player.dextrisity,
            strength=player.strength,
            level=player.level,
        )
