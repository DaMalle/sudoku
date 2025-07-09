import tkinter as tk
from enum import Enum
from typing import Callable

from sudoku.models.model import CellModel, MainModel, BoardModel
from sudoku.models.model import BoardValue


class Width: # const values
    MARGIN = 20
    CELL = 50
    GRID = 9 * CELL
    BOARD = 2 * MARGIN + GRID


class Difficulty(Enum):
    EASY   = 1
    MEDIUM = 2
    HARD   = 3
    EXPERT = 4


class BoardView(tk.Canvas):
    def __init__(self, root: tk.Tk, board_model: BoardModel) -> None:
        super().__init__(root)
        self.configure_view()
        self.draw_ui()

        self.root = root
        self.board_model = board_model
        self.cursor = (0, 0)

        self.update_cursor(self.cursor[0], self.cursor[1])
        self.update_board()

        self.pack()

    def configure_view(self) -> None:
        self["bg"] = "white"
        # self["highlightbackground"] = "white"
        self["width"] = Width.BOARD
        self["height"] = Width.BOARD

    def update_board(self) -> None:
        self.delete("puzzle")

        for y in range(9):
            for x in range(9):
                self._fill_cell(x, y, self.board_model.get_cell(x, y))

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


    def get_cursor(self) -> tuple[int, int]:
        return self.cursor

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
        self.cursor = (x, y)


    def draw_ui(self) -> None:
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
        super().__init__(root)
        self.root = root

        self["width"] = Width.BOARD
        self["height"] = Width.CELL
        self["bg"] = "white"
        # self["highlightbackground"] = "white"
        self.pack_propagate(False)
        self.pack()


class MainView(tk.Tk):
    """Root of the GUI"""

    def __init__(self, model: MainModel) -> None:
        super().__init__()
        self._configure_settings()
        self.model: MainModel = model

        self.opt = tk.StringVar(value=Difficulty.EASY.name.title())
        self.options = (d.name.title() for d in Difficulty)

        top_bar = TopBar(self)
        self.menu = tk.OptionMenu(top_bar, self.opt, *self.options)
        self.menu.pack(side="left", anchor="center")

        self.menu.config(
            bg="white", fg="black",
            activebackground="white", activeforeground="black",
            highlightthickness=1, relief="flat", bd=0
        )
        self.menu["menu"].config(
            bg="white", fg="black",
            activebackground="white", activeforeground="black",
            relief="flat", bd=0, tearoff=0)


        self._board = BoardView(self, self.model.board_model)

    @property
    def board(self) -> BoardView:
        return self._board

    def show_win_page(self) -> None:
        print("Won")

    def bind_key(self, key: str, command: Callable):
        self.bind(key, command)

    def run(self) -> None:
        self.mainloop()

    def _configure_settings(self) -> None:
        self.title("Sudoku")
        self.geometry("1000x1000")
        self["bg"] = "white"
        self["highlightbackground"] = "white"
