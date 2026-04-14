from dataclasses import dataclass

from domian.value_objects.enums import DefaultRotation

ROTATION_STEP: int = 90


@dataclass
class Rotation:
    angle: float = DefaultRotation.SOUTH
