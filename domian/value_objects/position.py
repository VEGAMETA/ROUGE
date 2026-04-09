from dataclasses import dataclass


@dataclass
class Size:
    width: int = 0
    height: int = 0


@dataclass
class Position:
    x: int = 0
    y: int = 0
