from domain.entities.statistics import Statistics
from domain.rules.progression import MAX_LEVEL


class RunSummary:
    LABEL_TIME: str = "Time"
    LABEL_LEVEL: str = "Level"
    LABEL_TREASURE: str = "Treasure"
    LABEL_ENEMIES: str = "Enemies"
    LABEL_FOOD: str = "Food"
    LABEL_ELIXIRS: str = "Elixirs"
    LABEL_SCROLLS: str = "Scrolls"
    LABEL_ATTACKS: str = "Attacks"
    LABEL_HITS: str = "Hits"
    LABEL_TILES: str = "Tiles"

    @staticmethod
    def format(statistics: Statistics, points: int, time: float) -> str:
        lines = [
            f"{RunSummary.LABEL_TIME}: {time:.2f}",
            f"{RunSummary.LABEL_LEVEL}: {statistics.level_reached}/{MAX_LEVEL}",
            f"{RunSummary.LABEL_TREASURE}: {points}",
            f"{RunSummary.LABEL_ENEMIES}: {statistics.enemies_defeated}",
            f"{RunSummary.LABEL_FOOD}: {statistics.food_consumed}",
            f"{RunSummary.LABEL_ELIXIRS}: {statistics.elixirs_used}",
            f"{RunSummary.LABEL_SCROLLS}: {statistics.scrolls_read}",
            f"{RunSummary.LABEL_ATTACKS}: {statistics.attacks_made}",
            f"{RunSummary.LABEL_HITS}: {statistics.hits_taken}",
            f"{RunSummary.LABEL_TILES}: {statistics.tiles_traversed}",
        ]
        return "\n".join(lines)
