from dataclasses import dataclass

from domain.entities.stairs import Stairs


@dataclass
class StairsDTO:
    x: int
    y: int
    type: int
    explored: bool


class StairsMapper:
    @staticmethod
    def to_dto(stairs: Stairs):
        return StairsDTO(
            x=stairs.position.x,
            y=stairs.position.y,
            type=stairs.type,
            explored=stairs.explored,
        )
