import random


class SudokuModel:
    def __init__(self) -> None:
        self._solution_generator = SolutionGenerator()

        self._solution: tuple[int, ...] | None = None
        self._game_board: list[int] | None = None

    @property
    def board(self) -> list[int] | None:
        return self._game_board

    @property
    def solution(self) -> tuple[int, ...] | None:
        return self._solution


class SolutionGenerator:
    def __init__(self) -> None:
        self._BOX_SIDE = 3
        self._GRID_SIDE = 9
        self._GRID = 81

    def create(self) -> tuple[int, ...]:
        pass

        return (0, 0, 0) # TODO: complete function


class BoardGenerator:
    def __init__(self) -> None:
        pass
