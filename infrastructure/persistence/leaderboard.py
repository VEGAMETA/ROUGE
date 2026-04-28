from pathlib import Path

LEADERBOARD_FILE = "save/leaderboard.txt"


class Leaderboard:
    @staticmethod
    def append(name: str, points: int) -> None:
        Path(LEADERBOARD_FILE).parent.mkdir(parents=True, exist_ok=True)
        with open(LEADERBOARD_FILE, "a") as f:
            f.write(f"{name} {points}\n")

    @staticmethod
    def read() -> list[str]:
        if not Path(LEADERBOARD_FILE).exists():
            return []
        with open(LEADERBOARD_FILE, "r") as f:
            return f.read().splitlines()
