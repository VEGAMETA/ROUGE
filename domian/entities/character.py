from domian.entities.backpack import Backpack
from domian.entities.weapon import Weapon


class Character:
    def __init__(
        self,
        health: int = 5,
        max_health: int = 5,
        dextrisity: int = 1,
        strength: int = 1,
        weapon: Weapon = None,
    ) -> None:
        self.health: int = health
        self.max_health: int = max_health
        self.dextrisity: int = dextrisity
        self.strength: int = strength
        self.weapon: Weapon | None = weapon
        self.inventory: Backpack = Backpack()
