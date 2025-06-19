import random
from copy import deepcopy


class SudokuModel:
    def __init__(self) -> None:
        self._solution_generator = SolutionGenerator(rng=random)

        self._solution: tuple[tuple[int, ...], ...] | None = None
        self._game_board: list[list[int]] | None = None

    @property
    def board(self) -> list[list[int]] | None:
        return self._game_board

    @property
    def solution(self) -> tuple[tuple[int, ...], ...] | None:
        return self._solution


class SolutionGenerator:
    def __init__(self, rng=random) -> None:
        self.rng = rng

    def create(self) -> tuple[tuple[int, ...], ...]:
        """
        Returns a valid sudoku solution as a 1D tuple of 81 elements,
        where each group of 9 represents a row.
        """

        n = [0, 1, 2]

        # Column groups are [ 0, 1, 2 | 3, 4, 5 | 6, 7, 8 ],
        # column_order shuffles the order of the column within each group
        # and the order of the groups
        column_order = tuple(group * 3 + column
            for group in self._shuffle(n)
            for column in self._shuffle(n)
        ) # Example: [ 2, 1, 0 | 7, 6, 8 | 4, 3, 5 ]

        row_order = tuple(group * 3 + row
            for group in self._shuffle(n)
            for row in self._shuffle(n)
        )

        pattern = lambda r, c: (3 * (r % 3) + r // 3 + c) % 9
        seed = self._shuffle(list(range(1, 10, 1)))

        solution = tuple(
            tuple(seed[pattern(r, c)] for c in column_order) for r in row_order
        )
        return solution

    def _shuffle(self, numbers: list[int]) -> list[int]:
        """
        Shuffles the order of elements in a list. Only used for integers,
        but would work with other types
        """

        return self.rng.sample(numbers, len(numbers))


class BoardGenerator:
    def __init__(self, solution: tuple[tuple[int, ...], ...]) -> None:
        self.solution = solution

    def create(self) -> list[list[int]] | None: #TODO: finish
        return


class SudokuSolver:
    def __init__(self, board: list[list[int]]) -> None:
        self.board = board
        self.EMPTY_CELL = 0

    def solve(self) -> bool:
        empty = self._find_empty()
        if empty is None:
            return True

        row, col = empty
        for num in range(1, 10, 1):
            if self._is_valid(num, row, col):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = self.EMPTY_CELL
        return False

    def _find_empty(self) -> tuple[int, int] | None:
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == self.EMPTY_CELL:
                    return (r, c)
        return None

    def _is_valid(self, num: int, row_index: int, column_index: int) -> bool:
        # Check row and column
        if num in self.board[row_index]:
            return False
        if num in (self.board[i][column_index] for i in range(9)):
            return False

        # Check 3x3 box
        start_row, start_col = 3 * (row_index // 3), 3 * (column_index // 3)
        for r in range(3):
            for c in range(3):
                if self.board[start_row + r][start_col + c] == num:
                    return False
        return True

if __name__ == "__main__":
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    solver = SudokuSolver(board=puzzle)
    solver.solve()
    for row in solver.board:
        print(row)
