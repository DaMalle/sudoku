import tkinter as tk
from enum import Enum
from typing import Callable

from sudoku.models.model import CellModel, MainModel, BoardModel
from sudoku.models.model import BoardValue


class Width: # const values
    """Contains constant side lengths used in the View"""
    MARGIN = 20
    CELL = 50
    GRID = 9 * CELL
    BOARD = 2 * MARGIN + GRID


class Difficulty(Enum):
    EASY   = "Easy"
    MEDIUM = "Medium"
    HARD   = "Hard"
    EXPERT = "Expert"


class BoardView(tk.Canvas):
    def __init__(self, root: tk.Tk, board_model: BoardModel) -> None:
        super().__init__(root)
        self._configure_view()
        self._draw_ui()

        self._board_model = board_model
        self._cursor = (0, 0)

        self.update_cursor(self._cursor[0], self._cursor[1])
        self.update_board()

        self.pack()

    def _configure_view(self) -> None:
        self["bg"] = "white"
        self["width"] = Width.BOARD
        self["height"] = Width.BOARD

    def update_board(self) -> None:
        """ Used for updating cells on the board
        and clearing winscreen after starting new game
        """
        self.delete("puzzle")
        self.delete("win_screen")

        for y in range(9):
            for x in range(9):
                self._fill_cell(x, y, self._board_model.get_cell(x, y))

    def _fill_cell(self, x, y, cell: CellModel):
        number = cell.current
        if number != BoardValue.EMPTY_CELL:
            self.create_text(
                # at the center:
                x * Width.CELL + Width.MARGIN + Width.CELL // 2,
                y * Width.CELL + Width.MARGIN + Width.CELL // 2,
                text=number, tags="puzzle",
                fill="black" if cell.is_clue else "blue",
                font=("Arial", Width.CELL // 4)
            )
    def draw_win_screen(self) -> None:
        """Draws a white box infront of the board with a text=You Won!"""
        self.create_rectangle(
            0, 0, Width.BOARD+1, Width.BOARD+1,
            fill="white", tags="win_screen"
        )
        self.create_text(
            Width.BOARD // 2, Width.BOARD // 2,
            text="You Won!", tags="win_screen"
        )


    def get_cursor(self) -> tuple[int, int]:
        return self._cursor

    def update_cursor(self, x: int, y: int) -> None:
        """Draws a red square (cursor) at (x,y)"""

        self.delete("cursor") # delete old cursor if any

        # x0, y0 represents the top left corner of the cell x, y are in
        y0 = Width.MARGIN + y * Width.CELL
        x0 = Width.MARGIN + x * Width.CELL

        self.create_rectangle( # the 1's keep the rectangle within the cell boarder
            x0 + 1,
            y0 + 1,
            x0 + Width.CELL - 1,
            y0 + Width.CELL - 1,
            width=2, outline="red", tags="cursor"
        )
        self._cursor = (x, y)


    def _draw_ui(self) -> None:
        """Draw the grid lines for the sudoku board"""

        for i in range(10):
            if i % 3 == 0: # is ith line a subgrid border line
                self._draw_vertical_line(index=i, fill="black", width=2)
                self._draw_horizontal_line(index=i, fill="black", width=2)
            else:
                self._draw_vertical_line(index=i, fill="gray", width=1)
                self._draw_horizontal_line(index=i, fill="gray", width=1)

    def _draw_vertical_line(self, index: int, fill: str, width: int) -> None:
        self.create_line(
            Width.MARGIN + index * Width.CELL,
            Width.MARGIN,
            Width.MARGIN + index * Width.CELL,
            Width.BOARD - Width.MARGIN,
            fill=fill, width=width
        )

    def _draw_horizontal_line(self, index: int, fill: str, width: int) -> None:
        self.create_line(
            Width.MARGIN,
            Width.MARGIN + index * Width.CELL,
            Width.BOARD - Width.MARGIN,
            Width.MARGIN + index * Width.CELL,
            fill=fill, width=width
        )


class TopBar(tk.Frame):
    def __init__(self, root: tk.Tk) -> None:
        """Container with the same with as the board"""

        super().__init__(root)

        self["width"] = Width.BOARD
        self["height"] = Width.CELL
        self["bg"] = "white"

        self.pack_propagate(False)
        self.pack()


class NewGameButton(tk.Button):
    def __init__(self, root: tk.Frame) -> None:
        super().__init__(root)
        self._configure_settings()
        self.pack(side="right", anchor="center")

    def set_command(self, command: Callable) -> None:
        self["command"] = command

    def _configure_settings(self) -> None:
        self["height"] = 1
        self["text"] = "New Game"
        self["bg"] = "white"
        self["fg"] = "black"
        self["activeforeground"] = "black"
        self["activebackground"] = "white"
        self["highlightthickness"] = 1
        self["relief"] = "flat"
        self["bd"] = 0


class DifficultyMenu(tk.OptionMenu):
    def __init__(self, root: tk.Frame) -> None:
        self._current = tk.StringVar(value=Difficulty.EASY.value)
        options = (d.value for d in Difficulty)
        super().__init__(root, self._current, *options)

        self._configure_settings()
        self.pack(side="left", anchor="center")

    def get_current_difficulty(self) -> Difficulty:
        return Difficulty(self._current.get())

    def bind_update_difficulty(self, func: Callable) -> None:
        self._current.trace_add("write", func)

    def _configure_settings(self) -> None:
        self["height"] = 1
        self["bg"] = "white"
        self["fg"] = "black"
        self["activeforeground"] = "black"
        self["activebackground"] = "white"
        self["highlightthickness"] = 1
        self["relief"] = "flat"
        self["bd"] = 0

        self["menu"]["bg"] = "white"
        self["menu"]["fg"] = "black"
        self["menu"]["activeforeground"] = "black"
        self["menu"]["activebackground"] = "white"
        self["menu"]["relief"] = "flat"
        self["menu"]["bd"] = 0
        self["menu"]["tearoff"] = 0


class MainView(tk.Tk):
    """Root of the GUI"""

    def __init__(self, model: MainModel) -> None:
        super().__init__()
        self._configure_settings()
        self.model: MainModel = model

        top_bar = TopBar(self)
        self._difficulty_menu = DifficultyMenu(top_bar)
        self._new_game_button = NewGameButton(top_bar)

        self._board = BoardView(self, self.model.board_model)

    @property
    def new_game_button(self) -> NewGameButton:
        return self._new_game_button

    @property
    def difficulty_menu(self) -> DifficultyMenu:
        return self._difficulty_menu

    @property
    def board(self) -> BoardView:
        return self._board

    def show_win_page(self) -> None:
        self.board.draw_win_screen()

    def bind_key(self, key: str, command: Callable):
        self.bind(key, command)

    def run(self) -> None:
        self.mainloop()

    def _configure_settings(self) -> None:
        self.title("Sudoku")
        self.geometry("1000x1000")
        self["bg"] = "white"
        self["highlightbackground"] = "white"
