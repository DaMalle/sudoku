import tkinter as tk
from enum import Enum


class Width:
    MARGIN = 20
    CELL = 50
    GRID = 9 * CELL
    BOARD = 2 * MARGIN + GRID


class Difficulty(Enum):
    EASY   = 1
    MEDIUM = 2
    HARD   = 3
    EXPERT = 4


class Board(tk.Canvas):
    def __init__(self, root: tk.Tk, initial_board_values) -> None:
        super().__init__(root)
        self.root = root
        self.initial_board_values = initial_board_values

        self.cursor = (0, 0)

        self._configure_widget()
        self._draw_initial_values(initial_board_values)
        self._draw_grid_lines()
        self._update_cursor(self.cursor[0], self.cursor[1])
        self.pack()

    def get_cursor(self) -> tuple[int, int]:
        return self.cursor

    def _update_cursor(self, x: int, y: int) -> None:
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

    def update_cell(self, x: int, y: int, number: int) -> None:
        self.delete(f"cell{x}{y}")

        self.create_text(
            x * Width.CELL + Width.MARGIN + Width.CELL // 2,
            y * Width.CELL + Width.MARGIN + Width.CELL // 2,
            text=number, tags=f"cell{x}{y}", font=("Arial", Width.CELL // 4)
        )

    def _configure_widget(self) -> None:
        self["bg"] = "white"
        # self["highlightbackground"] = "white"
        self["width"] = Width.BOARD
        self["height"] = Width.BOARD

    def _draw_grid_lines(self) -> None:
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

    def _draw_initial_values(self, initial_board_values) -> None:
        for iy, row in enumerate(initial_board_values):
            for ix, number in enumerate(row):
                if number != 0:
                    x = ix * Width.CELL + Width.MARGIN + Width.CELL // 2
                    y = iy * Width.CELL + Width.MARGIN + Width.CELL // 2
                    self.create_text(x, y, text=number, font=("Arial", Width.CELL // 4))

class TopBar(tk.Frame):
    def __init__(self, root: tk.Tk):
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

    def __init__(self) -> None:
        super().__init__()
        self._configure_settings()

        self.opt = tk.StringVar(value=Difficulty.EASY.name.title())
        self.options = (d.name.title() for d in Difficulty)

        top_bar = TopBar(self)
        self.menu = tk.OptionMenu(top_bar, self.opt, *self.options)
        self.menu.pack(side="left", anchor="center")


        # fill
        self.initial_board = tuple(tuple(0 for _ in range(9)) for _ in range(9))

        self.board = Board(self, self.initial_board)

    def run(self):
        self.mainloop()


    def _configure_settings(self) -> None:
        self.title("Sudoku")
        self.geometry("1000x1000")
        self["bg"] = "white"
        self["highlightbackground"] = "white"


if __name__ == "__main__":
    MainView().run()
