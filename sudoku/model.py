import random


class SudokuModel:
    def __init__(self) -> None:
        self._solution_generator = SolutionGenerator

        self._solution: tuple[int, ...] | None = None
        self._game_board: list[int] | None = None

    @property
    def board(self) -> list[int] | None:
        return self._game_board

    @property
    def solution(self) -> tuple[int, ...] | None:
        return self._solution


class SolutionGenerator:
    def create(self) -> tuple[int, ...]:
        """Creates a valid sudoku solution as a 1D tuple of 81 elements, where each group of 9 represents a row."""

        n = [0, 1, 2]

        # Column groups are [(0, 1, 2), (3, 4, 5), (6, 7, 8)], split based on which box the column is in.
        # column order shuffles the order of the column within each group and the order of the groups
        column_order = tuple(group * 3 + column
            for group in self._shuffle(n)
            for column in self._shuffle(n)
        )

        row_order = tuple(group * 3 + row
            for group in self._shuffle(n)
            for row in self._shuffle(n)
        )

        pattern = lambda r, c: (3 * (r % 3) + r // 3 + c) % 9
        seed = self._shuffle(list(range(1, 10, 1))) # numbers for the first row, with unshuffled columns

        solution = tuple(
            seed[pattern(r, c)]
            for c in column_order
            for r in row_order
        )
        return solution

    def _shuffle(self, numbers: list[int]) -> list[int]:
        """Shuffles the order of elements in a list. Only used for integers, but would work with other types"""

        return random.sample(numbers, len(numbers))


class BoardGenerator:
    def __init__(self) -> None:
        pass
