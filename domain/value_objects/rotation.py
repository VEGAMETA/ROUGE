from dataclasses import dataclass

from domain.value_objects.enums import DefaultRotation

ROTATION_STEP: int = 90


@dataclass
class Rotation:
    angle: float = DefaultRotation.SOUTH
