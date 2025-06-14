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
        _shuffle = lambda nums: random.sample(nums, len(nums))

        n = [0, 1, 2]
        column_order = tuple(g * 3 + c
            for g in _shuffle(n)
            for c in _shuffle(n)
        )

        row_order = tuple(g * 3 + r
            for g in _shuffle(n)
            for r in _shuffle(n)
        )

        _apply_pattern = lambda r, c: (3 * (r % 3) + r // 3 + c) % 9

        shuffled = _shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9])
        solution = tuple(
            shuffled[_apply_pattern(r, c)]
            for c in column_order
            for r in row_order
        )
        return solution


class BoardGenerator:
    def __init__(self) -> None:
        pass
