import tkinter as tk
from enum import Enum, auto

from sudoku.views.view import Difficulty, MainView, BoardView, Width, DifficultyMenu
from sudoku.models.model import MainModel, BoardModel


class State(Enum):
    HAS_WON = auto()
    PLAYING = auto()


def run_if_state_is_playing(func):
    def wrapper(self, *args, **kwargs):
        if self.state == State.PLAYING:
            return func(self, *args, **kwargs)
    return wrapper


class MainController:
    def __init__(self, model: MainModel, view: MainView) -> None:
        self.model: MainModel = model
        self.board_model: BoardModel = self.model.board_model
        self.view: MainView = view
        self.board_view: BoardView = self.view.board
        self.difficulty_menu: DifficultyMenu = self.view.difficulty_menu
        self.state = State.PLAYING

        self._setup_on_difficulty_change()
        self._setup_new_game()

        # set initial game
        self._update_difficulty()

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

    def _setup_new_game(self) -> None:
        self.view.new_game_button.set_command(self._update_difficulty)

    def _start_new_game(self) -> None:
        self.board_model.create_puzzle()

    def _setup_on_difficulty_change(self) -> None:
        self.difficulty_menu.bind_update_difficulty(self._update_difficulty)

    def _update_difficulty(self, *_) -> None:
        difficulty: Difficulty = self.difficulty_menu.get_current_difficulty()

        clues = 38
        match difficulty:
            case Difficulty.EASY:
                clues = 38
            case Difficulty.MEDIUM:
                clues = 36
            case Difficulty.HARD:
                clues = 34
            case Difficulty.EXPERT:
                clues = 31

        self.board_model.create_puzzle(clues=clues)
        self.board_view.update_board()
        self.state = State.PLAYING

    @run_if_state_is_playing
    def _handle_mouse_click(self, event: tk.Event) -> None:
        if event.widget == self.board_view:
            self._move_cursor_with_mouse(event)

    def _move_cursor_with_mouse(self, event: tk.Event) -> None:

        # check if mouse clicked on the board and not the margin around
        x_is_on_board = (Width.MARGIN < event.x < Width.GRID + Width.MARGIN)
        y_is_on_board = (Width.MARGIN < event.y < Width.GRID + Width.MARGIN)
        if x_is_on_board and y_is_on_board:
            y = (event.y - Width.MARGIN) // Width.CELL
            x = (event.x - Width.MARGIN) // Width.CELL
            self.board_view.update_cursor(x, y)


    @run_if_state_is_playing
    def _handle_number_input(self, number: int) -> None:
        """Used for binding (0-9) key press to insert (1-9 or clearing cell) into board"""

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
            self.state = State.HAS_WON

    @run_if_state_is_playing
    def _handle_move_cursor(self, x_delta: int, y_delta: int) -> None:
        """Handle arrow key navigation"""

        current_row, current_column = self.board_view.get_cursor()
        if current_row is not None and current_column is not None:
            upper = 8 # upper index bound
            lower = 0 # lower index bound

            new_row = max(lower, min(upper, current_row + x_delta))
            new_column = max(lower, min(upper, current_column + y_delta))

            self.board_view.update_cursor(new_row, new_column)
