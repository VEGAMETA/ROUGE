# audio_process.py

import time
from multiprocessing import Process, SimpleQueue
from pathlib import Path
from threading import Thread
from typing import Dict

from simpleaudio import WaveObject

from domain.value_objects.enums import SoundType

FILES: Dict[SoundType, Path] = {
    SoundType.MUSIC: Path("./static/audio/music/dungeon-ambience.wav"),
    SoundType.MOVE: Path("./static/audio/sfx/move.wav"),
    SoundType.SWING: Path("./static/audio/sfx/swing.wav"),
    SoundType.HIT: Path("./static/audio/sfx/hit.wav"),
    SoundType.DEATH: Path("./static/audio/sfx/death.wav"),
    SoundType.ITEM_PICK: Path("./static/audio/sfx/item_pick.wav"),
    SoundType.ITEM_USE: Path("./static/audio/sfx/item_use.wav"),
    SoundType.KILL: Path("./static/audio/sfx/kill.wav"),
    SoundType.LEVEL_UP: Path("./static/audio/sfx/stairs.wav"),
    SoundType.UI: Path("./static/audio/sfx/ui.wav"),
}


class Mixer(Process):
    def __init__(self, q: SimpleQueue):
        super().__init__(daemon=True)
        self.q = q
        self.sounds: Dict[SoundType, WaveObject] = {}

        self.running = True
        self.loop_music = True

    def load(self):
        for k, path in FILES.items():
            self.sounds[k] = WaveObject.from_wave_file(path.as_posix())

    def _play_loop(self, sound: WaveObject):
        while self.loop_music and self.running:
            play_obj = sound.play()
            play_obj.wait_done()

    def run(self):
        self.load()

        while self.running:
            try:
                time.sleep(0.001)
                effect = self.q.get()
            except:
                continue

            if effect is None:
                break

            sound = self.sounds.get(effect)
            if not sound:
                continue

            if effect == SoundType.MUSIC:
                Thread(target=self._play_loop, args=(sound,)).start()

            else:
                sound.play()
