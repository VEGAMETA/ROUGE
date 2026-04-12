from abc import ABC, abstractmethod

from domian.value_objects.position import Direction


class EnemyAI(ABC):
    @abstractmethod
    def next_direction(self, context) -> Direction: ...


class ZombieAI(EnemyAI):
    def next_direction(self, context) -> Direction:
        # Implement ZOMBIE AI logic here
        pass


class VampireAI(EnemyAI):
    def next_direction(self, context) -> Direction:
        # Implement VAMPIRE AI logic here
        pass


class GhostAI(EnemyAI):
    def next_direction(self, context) -> Direction:
        # Implement GHOST AI logic here
        pass


class OgreAI(EnemyAI):
    def next_direction(self, context) -> Direction:
        # Implement OGRE AI logic here
        pass


class SnakeMageAI(EnemyAI):
    def next_direction(self, context) -> Direction:
        # Implement SNAKE MAGE AI logic here
        pass
