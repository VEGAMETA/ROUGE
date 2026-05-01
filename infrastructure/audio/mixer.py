import time
from multiprocessing import Process, Queue
from pathlib import Path
from queue import Empty

from simpleaudio import PlayObject, WaveObject, stop_all

from domain.value_objects.enums import SoundType

FILES: dict[SoundType, Path] = {
    SoundType.STOP: Path("./static/audio/sfx/death.wav"),
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
    SoundType.DOOR: Path("./static/audio/sfx/door.wav"),
}


class Mixer(Process):
    def __init__(self, q: Queue) -> None:
        super().__init__(daemon=True)
        self.q = q
        self.sounds: dict[SoundType, WaveObject] = {}
        self.loop_objects: dict[WaveObject, PlayObject] = {}
        self.running: bool = True

    def load(self) -> None:
        for k, path in FILES.items():
            self.sounds[k] = WaveObject.from_wave_file(path.as_posix())

    def _play_loop(self):
        for sound, playing in self.loop_objects.items():
            if playing.is_playing():
                continue
            self.loop_objects[sound] = sound.play()

    def stop(self) -> None:
        self.running = False
        for playing in self.loop_objects.values():
            if not playing.is_playing():
                continue
            playing.stop()
        stop_all()

    def run(self) -> None:
        self.load()

        while self.running:
            try:
                self._play_loop()
                time.sleep(0.05)
                effect = self.q.get_nowait()
            except Empty:
                continue
            if not effect:
                continue
            if effect == SoundType.STOP:
                self.stop()
                break
            sound = self.sounds.get(effect)
            if not sound:
                continue
            playing = sound.play()
            if effect == SoundType.MUSIC:
                self.loop_objects[sound] = playing
