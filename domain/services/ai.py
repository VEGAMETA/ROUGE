from abc import ABC, abstractmethod

# circular import
from typing import TYPE_CHECKING

from domain.value_objects.position import Direction

if TYPE_CHECKING:
    from domain.entities.game_session import GameSession


class EnemyAI(ABC):
    @staticmethod
    @abstractmethod
    def next_direction(self, context: "GameSession") -> Direction: ...


class ZombieAI(EnemyAI):
    @staticmethod
    def next_direction(self, context: "GameSession") -> Direction:
        # Implement ZOMBIE AI logic here
        pass


class VampireAI(EnemyAI):
    @staticmethod
    def next_direction(self, context: "GameSession") -> Direction:
        # Implement VAMPIRE AI logic here
        pass


class GhostAI(EnemyAI):
    @staticmethod
    def next_direction(self, context: "GameSession") -> Direction:
        # Implement GHOST AI logic here
        pass


class OgreAI(EnemyAI):
    @staticmethod
    def next_direction(self, context: "GameSession") -> Direction:
        # Implement OGRE AI logic here
        pass


class SnakeMageAI(EnemyAI):
    @staticmethod
    def next_direction(self, context: "GameSession") -> Direction:
        # Implement SNAKE MAGE AI logic here
        pass
