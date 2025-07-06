from abc import ABC, abstractmethod


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
