from pathlib import Path

from domain.value_objects.enums import SoundType
from infrastructure.audio.mixer import Mixer


class SoundAssembler:
    @staticmethod
    def assemble_sounds(mixer: Mixer) -> None:
        mixer.register(SoundType.MOVE, Path("./static/audio/sfx/move.wav"))
        mixer.register(SoundType.SWING, Path("./static/audio/sfx/swing.wav"))
        # mixer.register(SoundType.HIT, Path("static\\audio\sfx\hit.wav"))
        mixer.register(SoundType.DEATH, Path("./static/audio/sfx/death.wav"))
