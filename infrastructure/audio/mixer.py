from threading import Thread
from queue import Queue
from typing import Dict
from simpleaudio import WaveObject

from domain.value_objects.enums import SoundType


class Mixer(Thread):
    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.sounds: Dict[SoundType, WaveObject] = {}
        self.q = Queue()
        self.running: bool = False

    def register(self, effect: SoundType, path: str) -> None:
        self.sounds[effect] = WaveObject.from_wave_file(str(path))

    def play(self, session: SoundType) -> None:
        for sound in session.sounds:
            if sound in self.sounds:
                self.q.put(sound)
        session.sounds.clear()

    def run(self) -> None:
        self.running = True
        while self.running:
            effect = self.q.get()
            if effect is None:
                break
            sound = self.sounds.get(effect)
            if sound:
                sound.play()
            self.q.task_done()

    def stop(self) -> None:
        self.running = False
        self.q.put(None)
