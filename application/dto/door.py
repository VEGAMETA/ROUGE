from dataclasses import dataclass

from domain.entities.door import Door


@dataclass
class DoorDTO:
    x: int
    y: int
    is_locked: bool
    type: int


class DoorMapper:
    @staticmethod
    def to_dto(door: Door) -> DoorDTO:
        return DoorDTO(
            x=door.position.x,
            y=door.position.y,
            is_locked=door.is_locked,
            type=door.type.value,
        )
