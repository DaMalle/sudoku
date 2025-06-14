import random
from collections import deque


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
        row = deque(range(1, 10, 1))
        solution = []

        for _ in range(3):
            for _ in range(3):
                solution += list(row)
                row.rotate(-3)
            row.rotate(1)

        return tuple(solution)


class BoardGenerator:
    def __init__(self) -> None:
        pass

SolutionGenerator().create()
