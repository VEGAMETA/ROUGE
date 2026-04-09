from dataclasses import dataclass


@dataclass(frozen=True)
class Constant:
    PI: float = 3.14159265359
    MINUS_PI: float = -3.14159265359
    INV_PI: float = 0.31830988618
    TWO_BY_PI: float = 0.636619772368
    TWO_BY_MINUS_PI: float = -0.636619772368
    PI_BY_2: float = 1.57079632679
    PI_BY_MINUS_2: float = -1.57079632679
    PI_BY_3: float = 1.0471975512
    PI_BY_MINUS_3: float = -1.0471975512
    PI_BY_4: float = 0.78539816339
    PI_BY_MINUS_4: float = -0.78539816339
    PI_MINUS_PI_BY_4: float = 2.35619449019
    PI_MINUS_PI_BY_MINUS_4: float = -2.35619449019
    PI_TIMES_2_BY_3: float = 2.09439510239
    PI_TIMES_2_BY_MINUS_3: float = -2.09439510239
    SQRT_TWO_BY_TWO: float = 0.70710678118
