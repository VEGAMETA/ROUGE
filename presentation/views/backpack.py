from abc import ABC, abstractmethod
from typing import Any, Optional


class BackpackView(ABC):
    @staticmethod
    @abstractmethod
    def show(
        window: Any, items: list, item_type: Any, equipped: Any = None
    ) -> Optional[int]: ...
