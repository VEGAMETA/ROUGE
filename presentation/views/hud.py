from abc import ABC, abstractmethod

from presentation.renderer import Renderer


class HUD(ABC):
    @abstractmethod
    def show(renderer: Renderer) -> None: ...
