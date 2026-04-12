from functools import partial
from threading import Event, Thread
from time import monotonic, sleep
from typing import Callable


class Timer:
    def __init__(
        self, duration: float = 1.0, callback: Callable = lambda: None, *args, **kwargs
    ) -> None:
        self.start_time: float = 0
        self.duration: float = duration
        self._is_running: bool = False
        self.callback: Callable = partial(callback, *args, **kwargs)
        self._stop_event = Event()
        self._thread: Thread = Thread(target=self._run, daemon=True)

    def start(self) -> None:
        self._stop_event.clear()
        self.start_time = monotonic()
        self._is_running: bool = True
        self._thread: Thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        if self._stop_event.wait(self.duration):
            return
        self.callback()

    def stop(self) -> None:
        self._stop_event.set()
        self._is_running = False

    @property
    def is_running(self) -> bool:
        return self._is_running

    @is_running.setter
    def is_running(self, value: bool) -> None:
        self._is_running = value
        if not value:
            self.stop()

    def is_expired(self) -> bool:
        return monotonic() >= self.duration + self.start_time

    def get_remaining_time(self) -> float:
        return max(0, self.duration - (monotonic() - self.start_time))

    def get_elapsed_time(self) -> float:
        return min(self.duration, monotonic() - self.start_time)

    @staticmethod
    def sleep_for(duration: float) -> None:
        if duration <= 0:
            return
        try:
            sleep(duration)
        except KeyboardInterrupt:
            pass
