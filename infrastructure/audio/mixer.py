from pathlib import Path
from queue import Queue
from threading import Thread
from typing import Dict

from simpleaudio import WaveObject

from domain.entities.game_session import GameSession
from domain.value_objects.enums import SoundType


class Mixer(Thread):
    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.sounds: Dict[SoundType, WaveObject] = {}
        self.q: Queue[SoundType] = Queue()
        self.running: bool = False

    def register(self, effect: SoundType, path: Path) -> None:
        self.sounds[effect] = WaveObject.from_wave_file(path.as_posix())

    def play(self, context: GameSession) -> None:
        for sound in context.sounds:
            if sound in self.sounds:
                self.q.put(sound)
        context.sounds.clear()

    def run(self) -> None:
        self.running = True
        while self.running:
            effect = self.q.get()
            if not effect:
                break
            if sound := self.sounds.get(effect):
                sound.play()
            self.q.task_done()

    def stop(self) -> None:
        self.running = False
        while not self.q.empty():
            self.q.get()

    def __del__(self) -> None:
        self.stop()
