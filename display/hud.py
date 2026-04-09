from classes.entities.player import Player


class HUD:
    def __init__(self, data: dict) -> None:
        self.data: dict = data
        self.player: Player | None = None

    def get_player(self, player: Player) -> None:
        self.player = player

    def display(self) -> None: ...
