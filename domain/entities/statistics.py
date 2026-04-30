from dataclasses import dataclass


@dataclass
class Statistics:
    treasure_collected: int = 0
    level_reached: int = 0
    enemies_defeated: int = 0
    food_consumed: int = 0
    elixirs_used: int = 0
    scrolls_read: int = 0
    attacks_made: int = 0
    hits_taken: int = 0
    tiles_traversed: int = 0
