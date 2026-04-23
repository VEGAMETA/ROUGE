from dataclasses import dataclass

TARGET_FPS: float = 60.0


@dataclass(frozen=True)
class Visuals:
    GLIMP_DENSITY: float = 0.01
    GLIMP_DENSITY_M: float = GLIMP_DENSITY * 0.1
