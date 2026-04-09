from abc import ABC


class EnemyAI(ABC):
    def next_move(self, enemy, context): ...
