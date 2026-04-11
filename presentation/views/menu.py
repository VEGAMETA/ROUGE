from abc import ABC, abstractmethod

from presentation.renderer import Renderer


class Menu(ABC):
    @abstractmethod
    def show(renderer: Renderer) -> None: ...
