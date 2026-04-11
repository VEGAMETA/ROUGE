from abc import ABC, abstractmethod


class EnemyAI(ABC):
    @abstractmethod
    def next_move(self, enemy, context): ...

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        return super().__eq__(other)


class ZombieAI(EnemyAI):
    def next_move(self, enemy, context):
        # Implement ZOMBIE AI logic here
        pass


class VampireAI(EnemyAI):
    def next_move(self, enemy, context):
        # Implement VAMPIRE AI logic here
        pass


class GhostAI(EnemyAI):
    def next_move(self, enemy, context):
        # Implement GHOST AI logic here
        pass


class OgreAI(EnemyAI):
    def next_move(self, enemy, context):
        # Implement OGRE AI logic here
        pass


class SnakeMageAI(EnemyAI):
    def next_move(self, enemy, context):
        # Implement SNAKE MAGE AI logic here
        pass
