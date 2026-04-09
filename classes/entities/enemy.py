import enum


class Hostility(enum.Enum):
    NEUTRAL = 0
    HOSTILE = 1
    FRIENDLY = 2


class EnemyType(enum.Enum):
    PASSIVE = 0
    AGGRESSIVE = 1
    COWARD = 2


class Enemy:
    def __init__(
        self,
        type_: EnemyType = EnemyType.PASSIVE,
        health: int = 5,
        dextrisity: int = 1,
        strength: int = 1,
        hostility: Hostility = Hostility.NEUTRAL,
    ) -> None:
        self.type: EnemyType = type_
        self.health: int = health
        self.dextrisity: int = dextrisity
        self.strength: int = strength
        self.hostility: int = hostility
