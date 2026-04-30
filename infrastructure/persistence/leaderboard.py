from dataclasses import dataclass
from pathlib import Path

from infrastructure.persistence.save_load import SaverLoader

LEADERBOARD_FILE = "save/leaderboard.json"


@dataclass
class LeaderboardRecord:
    name: str
    treasure: int
    level: int
    enemies: int
    food: int
    elixirs: int
    scrolls: int
    attacks: int
    hits: int
    tiles: int
    timestamp: str


class Leaderboard:
    @staticmethod
    def append(record: LeaderboardRecord) -> None:
        entries = Leaderboard._load_raw()
        entries.append(_record_to_dict(record))
        entries.sort(key=lambda r: r.get("treasure", 0), reverse=True)
        SaverLoader.save(LEADERBOARD_FILE, entries)

    @staticmethod
    def read() -> list[LeaderboardRecord]:
        entries = Leaderboard._load_raw()
        entries.sort(key=lambda r: r.get("treasure", 0), reverse=True)
        return [_record_from_dict(e) for e in entries]

    @staticmethod
    def _load_raw() -> list[dict]:
        if not Path(LEADERBOARD_FILE).exists():
            return []
        return SaverLoader.load(LEADERBOARD_FILE)


def _record_to_dict(record: LeaderboardRecord) -> dict:
    return {
        "name": record.name,
        "treasure": record.treasure,
        "level": record.level,
        "enemies": record.enemies,
        "food": record.food,
        "elixirs": record.elixirs,
        "scrolls": record.scrolls,
        "attacks": record.attacks,
        "hits": record.hits,
        "tiles": record.tiles,
        "timestamp": record.timestamp,
    }


def _record_from_dict(data: dict) -> LeaderboardRecord:
    return LeaderboardRecord(
        name=data.get("name", "?"),
        treasure=data.get("treasure", 0),
        level=data.get("level", 0),
        enemies=data.get("enemies", 0),
        food=data.get("food", 0),
        elixirs=data.get("elixirs", 0),
        scrolls=data.get("scrolls", 0),
        attacks=data.get("attacks", 0),
        hits=data.get("hits", 0),
        tiles=data.get("tiles", 0),
        timestamp=data.get("timestamp", ""),
    )
