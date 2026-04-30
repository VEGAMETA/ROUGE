from dataclasses import dataclass

from domain.entities.key import Key


@dataclass
class KeyDTO:
    x: int
    y: int
    type: int


class KeyMapper:
    @staticmethod
    def to_dto(key: Key):
        return KeyDTO(
            x=key.position.x,
            y=key.position.y,
            type=key.type.value,
        )
