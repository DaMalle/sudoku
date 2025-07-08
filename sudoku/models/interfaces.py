from abc import ABC, abstractmethod


class ICellModel(ABC):
    @property
    @abstractmethod
    def solution(self) -> int:
        pass

    @property
    @abstractmethod
    def current(self) -> int:
        pass

    @property
    @abstractmethod
    def is_clue(self) -> bool:
        pass

    @current.setter
    @abstractmethod
    def current(self, value: int) -> None:
        pass


class IBoardModel(ABC):
    @abstractmethod
    def get_cell(self, x: int, y: int) -> ICellModel:
        pass

    @abstractmethod
    def is_complete(self) -> bool:
        pass
