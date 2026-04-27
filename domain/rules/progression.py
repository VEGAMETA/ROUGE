from enum import IntEnum

ENEMY_HEALTH_FACTOR = 1.2
ENEMY_STATS_FACTOR = 5.6


class Level(IntEnum):
    LEVEL_1: int = 0
    LEVEL_2: int = 1
    LEVEL_3: int = 2
    LEVEL_4: int = 3
    LEVEL_5: int = 4
    LEVEL_6: int = 5
    LEVEL_7: int = 6
    LEVEL_8: int = 7
    LEVEL_9: int = 8
    LEVEL_10: int = 9
    LEVEL_11: int = 10
    LEVEL_12: int = 11
    LEVEL_13: int = 12
    LEVEL_14: int = 13
    LEVEL_15: int = 14
    LEVEL_16: int = 15
    LEVEL_17: int = 16
    LEVEL_18: int = 17
    LEVEL_19: int = 18
    LEVEL_20: int = 19
    LEVEL_21: int = 20


MAX_LEVEL = len(Level)
