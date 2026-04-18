from __future__ import annotations

from dataclasses import dataclass, field
from random import randint
from uuid import UUID, uuid4

from domain.rules.progression import Level
from domain.value_objects.position import Position
from domain.value_objects.size import Size


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


@dataclass(eq=False)
class Character(Entity2D):
    health: float
    max_health: float
    dexterity: int
    strength: int
    level: Level
