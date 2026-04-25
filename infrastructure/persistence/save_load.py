import json
from pathlib import Path


class SaverLoader:
    @staticmethod
    def save(filename: str, data: dict) -> None:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w") as f:
            f.write(json.dumps(data, indent=2))

    @staticmethod
    def load(filename: str) -> dict:
        with open(filename, "r") as f:
            return json.loads(f.read())
