from domain.value_objects.enums import SoundType
from infrastructure.audio.mixer import Mixer


class SoundAssembler:
    @staticmethod
    def assemble_sounds(mixer: Mixer) -> None:
        mixer.register(SoundType.MOVE, "static/audio/sfx/move.wav")
        mixer.register(SoundType.SWING, "static/audio/sfx/swing.wav")
