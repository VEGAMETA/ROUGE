import json


class Savefile:
    @staticmethod
    def save(filename: str, data: dict) -> None:
        with open(filename, "w") as f:
            f.write(json.dumps(data))

    @staticmethod
    def load(filename: str) -> dict:
        with open(filename, "r") as f:
            return json.loads(f.read())
