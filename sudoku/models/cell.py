class CellModel:
    def __init__(self, solution: int, current: int, is_clue: bool) -> None:
        self._solution = solution
        self._current = current
        self._is_clue = is_clue

    @property
    def solution(self) -> int:
        return self._solution

    @property
    def current(self) -> int:
        return self._current

    @current.setter
    def current(self, value: int) -> None:
        valid_values = list(range(0, 10, 1))
        if value not in valid_values:
            raise ValueError("Tried to insert invalid number")
        self._current = value

    @property
    def is_clue(self) -> bool:
        return self._is_clue
