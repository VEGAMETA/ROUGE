class Timings:
    TICKS_PER_SECOND: int = 240
    NANOSECONDS_PER_TICK: int = 1000000000 // TICKS_PER_SECOND
    MILLISECONDS_PER_TICK: float = 1000 / TICKS_PER_SECOND
    SECONDS_PER_TICK: float = 1 / TICKS_PER_SECOND


class Keymap:
    ACTIONS: dict = {
        "up": "w",
        "down": "s",
        "left": "a",
        "right": "d",
        "attack": "h",
        "use": "f",
        "inventory": "i",
        "food": "j",
        "elixir": "k",
        "scroll": "e",
    }
