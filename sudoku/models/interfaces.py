from abc import ABC, abstractmethod


class IBoardModel(ABC):
    @abstractmethod
    def create(self) -> None:
        pass
