from __future__ import annotations

from dataclasses import dataclass, field
from random import randint
from uuid import UUID, uuid4

from domain.rules.progression import Level
from domain.value_objects.position import Position
from infrastructure.vector import Size


@dataclass
class Entity:
    uuid: UUID = field(init=False, default_factory=uuid4, hash=True, compare=True)

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __eq__(self, other: Entity) -> bool:
        return self.uuid == other.uuid


@dataclass(eq=False)
class Entity2D(Entity):
    position: Position


@dataclass(eq=False)
class Shape2D(Entity2D):
    size: Size

    def get_random_inbound(self) -> Position:
        return Position(
            randint(*(Position(1, self.size.width - 1) + self.position.x)),
            randint(*(Position(1, self.size.height - 1) + self.position.y)),
        )

    def is_inbound(self, pos: Position) -> bool:
        x_min, x_max = self.position.x + 1, self.position.x + self.size.width - 1
        y_min, y_max = self.position.y + 1, self.position.y + self.size.height - 1
        return x_min <= pos.x <= x_max and y_min <= pos.y <= y_max


@dataclass(eq=False)
class Character(Entity2D):
    health: float
    max_health: float
    dexterity: int
    strength: int
    level: Level
