import random
from copy import deepcopy

from sudoku.models.cell import CellModel


class BoardValue: # constants
    EMPTY_CELL = 0


class BoardModel:
    def __init__(self) -> None:
        self._board: list[list[CellModel]] = [
            [CellModel(BoardValue.EMPTY_CELL, BoardValue.EMPTY_CELL, False)
                for _ in range(9)]
            for _ in range(9)
        ]

    def is_complete(self) -> bool:
        for y in range(9):
            for x in range(9):
                cell = self._board[y][x]
                if cell.current != cell.solution:
                    return False
        return True

    def get_cell(self, x: int, y: int) -> CellModel:
        return self._board[y][x]

    def create_puzzle(self, clues: int = 80) -> None:
        solution = SolutionGenerator().create()
        puzzle = PuzzleGenerator(solution).create(clues)
        for y in range(9):
            for x in range(9):
                self._board[y][x] = CellModel(
                    solution[y][x],
                    puzzle[y][x],
                    (puzzle[y][x] != BoardValue.EMPTY_CELL)
                )

class MainModel:
    def __init__(self) -> None:
        self._board_model: BoardModel = BoardModel()

    @property
    def board_model(self) -> BoardModel:
        return self._board_model


class SolutionGenerator:
    def __init__(self) -> None:
        self.rng = random

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

        return random.sample(numbers, len(numbers))


class PuzzleGenerator:
    def __init__(self, solution: tuple[tuple[int, ...], ...]) -> None:
        self._solution = solution

    def create(self, clues: int) -> list[list[int]]:
        while True:
            board = [ [BoardValue.EMPTY_CELL] * 9 for _ in range(9)] # empty 9x9
            self._fill_cells(board, clues)
            board_copy = deepcopy(board)

            if SudokuSolver(board).solve_multiple() == 1:
                return board_copy

    def _fill_cells(self, board: list[list[int]], fill_count: int = 0) -> None:
        all_cells = 81
        fill_count = min(all_cells, fill_count)

        for i in random.sample(range(all_cells), fill_count):
            board[i // 9][i % 9] = self._solution[i // 9][i % 9]


class SudokuSolver:
    def __init__(self, board: list[list[int]]) -> None:
        self.board = board
        self.empty_cells = self._get_empty_cells()

    def solve_multiple(self) -> int:
        if self.empty_cells == []:
            return 1

        counter = 0
        x, y = self.empty_cells.pop(0)
        for num in range(1, 10, 1):
            if self._is_valid(num, y, x):
                self.board[y][x] = num
                counter += self.solve_multiple()
                if self.empty_cells != []:
                    self.board[y][x] = BoardValue.EMPTY_CELL
                    self.empty_cells.insert(0, (x, y) )
        return counter

    def _get_empty_cells(self) -> list[tuple[int, int]]:
        empty_cells = [
            (x, y) for x in range(9) for y in range(9)
            if self.board[y][x] == BoardValue.EMPTY_CELL
        ]

        return empty_cells

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
