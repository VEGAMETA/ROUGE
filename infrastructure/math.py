from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class Constant:
    E: float = 2.71828182846
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


#  ^
# m\\
#  \ \
#  \  \
#  \   \
#  \    \
# -+------->
#  \0    m
def inv_linear(x: float, m: float = 0, k: float = 1) -> float:
    return m - k * x


#  ^
# m\   __
#  \  /  \
#  \ |    \
#  \/      \
# -+---------->
#  \0       m
def inv_parabola(x: float, m: float) -> float:
    return m - pow((m - 2 * x) / sqrt(m), 2)


#  ^
# m\   __
#  \  /
#  \ |
#  \/
# -+------->
#  \0    m
def exponent_saturation(x: float, m: float) -> float:
    return m - m * pow(1 - x / m, Constant.E)


#  ^
# m\     |
#  \    /
#  \   |
#  \__/
# -+------->
#  \0    m
def exponent(x: float, m: float) -> float:
    return m * pow(x / m, Constant.E)


def build_grid_graph(n: int) -> list[list[int]]:
    return [
        [
            j
            for j in (i - 1, i + 1, i - n, i + n)
            if 0 <= j < n * n
            and (j // n == i // n if abs(j - i) == 1 else abs(j - i) == n)
        ]
        for i in range(n * n)
    ]
