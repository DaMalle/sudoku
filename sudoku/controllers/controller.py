import tkinter as tk

from sudoku.views.view import MainView, BoardView, Width
from sudoku.models.model import MainModel, BoardModel


class MainController:
    def __init__(self, model: MainModel, view: MainView) -> None:
        self.model: MainModel = model
        self.board_model: BoardModel = self.model.board_model
        self.view: MainView = view
        self.board_view: BoardView = self.view.board

    def start_game(self) -> None:
        self._setup_keybinds()

        self.view.run()

    def _setup_keybinds(self) -> None:

        # did not work with for-loop...
        self.view.bind_key("0", lambda _: self._handle_number_input(0))
        self.view.bind_key("1", lambda _: self._handle_number_input(1))
        self.view.bind_key("2", lambda _: self._handle_number_input(2))
        self.view.bind_key("3", lambda _: self._handle_number_input(3))
        self.view.bind_key("4", lambda _: self._handle_number_input(4))
        self.view.bind_key("5", lambda _: self._handle_number_input(5))
        self.view.bind_key("6", lambda _: self._handle_number_input(6))
        self.view.bind_key("7", lambda _: self._handle_number_input(7))
        self.view.bind_key("8", lambda _: self._handle_number_input(8))
        self.view.bind_key("9", lambda _: self._handle_number_input(9))

        self.view.bind_key("<Button-1>", self._handle_mouse_click)

        self.view.bind_key("<Up>", lambda _: self._handle_move_cursor(0, -1))
        self.view.bind_key("<Down>", lambda _: self._handle_move_cursor(0, 1))
        self.view.bind_key("<Left>", lambda _: self._handle_move_cursor(-1, 0))
        self.view.bind_key("<Right>", lambda _: self._handle_move_cursor(1, 0))

    def _handle_mouse_click(self, event: tk.Event) -> None:
        if (Width.MARGIN < event.y < Width.GRID + Width.MARGIN and
            Width.MARGIN < event.x < Width.GRID + Width.MARGIN):
            x = (event.x - Width.MARGIN) // Width.CELL
            y = (event.y - Width.MARGIN) // Width.CELL
            self.view.board.update_cursor(x, y)

    def _handle_number_input(self, number: int) -> None:
        """Handle number key press"""

        x, y = self.board_view.get_cursor()
        if x is None or y is None:
            raise ValueError("The cursor is broken")

        elif not self.board_model.get_cell(x, y).is_clue:
            self._insert_number(x, y, number)

    def _insert_number(self, x: int, y: int, number: int) -> None:
        """Process inserting a number into the selected cell"""

        self.board_model.get_cell(x, y).current = number
        self.board_view.update_board()

        if self.board_model.is_complete():
            self.view.show_win_page()

    def _handle_move_cursor(self, x_delta: int, y_delta: int) -> None:
        """Handle arrow key navigation"""

        current_row, current_column = self.board_view.get_cursor()
        if current_row is not None and current_column is not None:
            upper = 8 # upper index bound
            lower = 0 # lower index bound

            new_row = max(lower, min(upper, current_row + x_delta))
            new_column = max(lower, min(upper, current_column + y_delta))

            self.board_view.update_cursor(new_row, new_column)
