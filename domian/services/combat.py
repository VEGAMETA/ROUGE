class CombatService:
    def attack(attacker, defender) -> None:
        if (
            not hasattr(defender, "health")
            or not hasattr(attacker, "strength")
            or not hasattr(defender, "dexterity")
        ):
            return
        defender.health -= attacker.strength
