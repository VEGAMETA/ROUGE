import time


class Timer:
    def __init__(self, duration: float) -> None:
        self.duration = duration
        self.start_time = time.time()

    def is_expired(self) -> bool:
        return time.time() - self.start_time >= self.duration

    def reset(self) -> None:
        self.start_time = time.time()

    def get_remaining_time(self) -> float:
        return self.duration - (time.time() - self.start_time)

    def get_elapsed_time(self) -> float:
        return time.time() - self.start_time

    @staticmethod
    def sleep_timer(duration: float) -> None:
        time.sleep(duration)
