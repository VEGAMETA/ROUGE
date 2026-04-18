from pathlib import Path

from domain.value_objects.enums import SoundType
from infrastructure.audio.mixer import Mixer


class SoundAssembler:
    @staticmethod
    def assemble_sounds(mixer: Mixer) -> None:
        mixer.register(
            SoundType.MUSIC, Path("./static/audio/music/dungeon-ambiance.wav")
        )
        mixer.register(SoundType.MOVE, Path("./static/audio/sfx/move.wav"))
        mixer.register(SoundType.SWING, Path("./static/audio/sfx/swing.wav"))
        mixer.register(SoundType.HIT, Path("./static/audio/sfx/hit.wav"))
        mixer.register(SoundType.DEATH, Path("./static/audio/sfx/death.wav"))
        mixer.register(SoundType.ITEM_PICK, Path("./static/audio/sfx/item_pick.wav"))
        mixer.register(SoundType.ITEM_USE, Path("./static/audio/sfx/item_use.wav"))
        mixer.register(SoundType.KILL, Path("./static/audio/sfx/kill.wav"))
        mixer.register(SoundType.LEVEL_UP, Path("./static/audio/sfx/stairs.wav"))
        mixer.register(SoundType.UI, Path("./static/audio/sfx/ui.wav"))
