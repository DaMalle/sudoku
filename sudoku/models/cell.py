class Cell:
    def __init__(self, solution_value: int, is_initial_cell: bool, current_value: int = 0) -> None:
        self._solution_value = solution_value
        self._is_initial_cell = is_initial_cell
        self._current_value = current_value

    @property
    def solution_value(self) -> int:
        return self._solution_value

    @property
    def is_initial_cell(self) -> int:
        return self._is_initial_cell

    @property
    def current_value(self) -> int:
        return self._current_value
