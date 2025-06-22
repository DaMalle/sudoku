import random
from copy import deepcopy


class SudokuModel:
    def __init__(self) -> None:
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


class SudokuSolver:
    def __init__(self, board: list[list[int]]) -> None:
        self.board = board
        self.EMPTY_CELL = 0

    def solve_multiple(self) -> int:
        empty = self._find_empty()
        if empty is None:
            return 1

        counter = 0
        row, col = empty
        for num in range(1, 10, 1):
            if self._is_valid(num, row, col):
                self.board[row][col] = num
                counter += self.solve_multiple()
                self.board[row][col] = self.EMPTY_CELL
        return counter

    def solve(self) -> bool:
        """Recursive solver using backtracking"""

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

    def _is_valid(self, num: int, y: int, x: int) -> bool:
        """Check if num is a valid number for the row, column and box"""

        # Check row and column
        if num in self.board[y]:
            return False
        if num in (self.board[i][x] for i in range(9)):
            return False

        # Check 3x3 box
        x0 = (y // 3) * 3
        y0 = (x // 3) * 3
        if num in (self.board[x0+c][y0+r] for c in range(3) for r in range(3)):
            return False

        return True


class BoardGenerator:
    def __init__(self, solution: tuple[tuple[int, ...], ...]) -> None:
        self._solution = solution

    def create(self, max_iterations: int = 1) -> list[list[int]] | None:
        for _ in range(max_iterations):
            board = [list(row) for row in self._solution]
            self._unfill_cells(board, 20)
            board_copy = deepcopy(board)

            if SudokuSolver(board).solve():
                return board_copy

        return None

    def _unfill_cells(self, board: list[list[int]], unfill_count: int = 0) -> None:
        for i in random.sample(range(81), unfill_count):
            board[i // 9][i % 9] = 0



if __name__ == "__main__":
    puzzle = [
        # [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],

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
    # print(solver.solve_multiple())
    # for row in solver.board:
        # print(row)
    new_board = BoardGenerator(tuple(tuple(row) for row in solver.board)).create(2)
    if new_board:
        for row in new_board:
            print(row)
