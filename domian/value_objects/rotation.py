from dataclasses import dataclass

from domian.value_objects.enums import DefaultRotation


@dataclass
class Rotation:
    ROTATION_STEP: int = 90
    angle: float = DefaultRotation.SOUTH
