from abc import ABC, abstractmethod
from typing import Callable


class IBoardView(ABC):
    @abstractmethod
    def configure_view(self) -> None:
        pass

    @abstractmethod
    def draw_ui(self) -> None:
        pass

    @abstractmethod
    def get_cursor(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def update_cursor(self, x, y) -> None:
        pass

    @abstractmethod
    def update_board(self) -> None:
        pass


class IMainView(ABC):
    @property
    @abstractmethod
    def board(self) -> IBoardView:
        pass

    @abstractmethod
    def show_win_page(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def bind_key(self, key: str, command: Callable) -> None:
        pass
