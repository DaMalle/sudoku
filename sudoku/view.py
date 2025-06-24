import tkinter as tk
from enum import Enum


class Length(Enum):
    """Different side lengths for the sudoku board"""
    MARGIN = 20
    CELL = 50
    GRID = CELL * 9
    BOARD = MARGIN + GRID + MARGIN


class Board(tk.Canvas):
    def __init__(self, root) -> None:
        super().__init__(root)
        self.root = root
        self._configure_widget()
        self._draw()
        self.draw_cursor(0, 0)

    def _draw(self) -> None:
        """Draw the grid lines for the sudoku board"""

        def _draw_vertical(index: int, fill: str, width: int) -> None:
            self.create_line(
                Length.MARGIN.value + index*Length.CELL.value,
                Length.MARGIN.value,
                Length.MARGIN.value + index*Length.CELL.value,
                Length.BOARD.value - Length.MARGIN.value,
                fill=fill, width=width
            )

        def _draw_horizontal(index: int, fill: str, width: int) -> None:
            self.create_line(
                Length.MARGIN.value,
                Length.MARGIN.value + index*Length.CELL.value,
                Length.BOARD.value - Length.MARGIN.value,
                Length.MARGIN.value + index*Length.CELL.value,
                fill=fill, width=width
            )

        for i in range(10):
            if i % 3 == 0: # is ith line a subgrid border line
                _draw_vertical(index=i, fill="black", width=2)
                _draw_horizontal(index=i, fill="black", width=2)
            else:
                _draw_vertical(index=i, fill="gray", width=1)
                _draw_horizontal(index=i, fill="gray", width=1)


    def _configure_widget(self) -> None:
        self["bg"] = "white"
        self["width"] = Length.BOARD.value
        self["height"] = Length.BOARD.value

    def draw_cursor(self, x: int, y: int) -> None:
        """Draws a red square (cursor) at (x,y)"""

        self.delete("cursor") # delete old cursor if any

        y0 = Length.MARGIN.value + y * Length.CELL.value
        x0 = Length.MARGIN.value + x * Length.CELL.value

        self.create_rectangle(
            x0 + 1,
            y0 + 1,
            x0 + Length.CELL.value - 1,
            y0 + Length.CELL.value - 1,
            width=2, outline="red", tags="cursor")




class MainApp(tk.Tk):
    """Root of the GUI"""

    def __init__(self) -> None:
        super().__init__()
        self._configure_widget()
        self._draw()
        self.mainloop()

    def _draw(self) -> None:
        board = Board(self)
        board.pack()

    def _configure_widget(self) -> None:
        self.title("Sudoku")
        # self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.geometry("1000x1000")
