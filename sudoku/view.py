import tkinter as tk


class Board(tk.Canvas):
    def __init__(self, root) -> None:
        super().__init__(root)
        self.root = root

        self._MARGIN = 20
        self._CELL_WIDTH = 50
        self._GRID_WIDTH = 9 * self._CELL_WIDTH
        self._BOARD_WIDTH = self._MARGIN * 2 + self._GRID_WIDTH

        self._configure_widget()
        self._draw()
        self.draw_cursor(0, 0)

    def _draw(self) -> None:
        """Draw the grid lines for the sudoku board"""

        def _draw_vertical(index: int, fill: str, width: int) -> None:
            self.create_line(
                self._MARGIN + index * self._CELL_WIDTH,
                self._MARGIN,
                self._MARGIN + index * self._CELL_WIDTH,
                self._BOARD_WIDTH - self._MARGIN,
                fill=fill, width=width
            )

        def _draw_horizontal(index: int, fill: str, width: int) -> None:
            self.create_line(
                self._MARGIN,
                self._MARGIN + index * self._CELL_WIDTH,
                self._BOARD_WIDTH - self._MARGIN,
                self._MARGIN + index * self._CELL_WIDTH,
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
        self["width"] = self._BOARD_WIDTH
        self["height"] = self._BOARD_WIDTH

    def draw_cursor(self, x: int, y: int) -> None:
        """Draws a red square (cursor) at (x,y)"""

        self.delete("cursor") # delete old cursor if any

        # x0, y0 represents the top left corner of the cell x, y are in
        y0 = self._MARGIN + y * self._CELL_WIDTH
        x0 = self._MARGIN + x * self._CELL_WIDTH

        self.create_rectangle( # the 1's keep the rectangle within the cell boarder
            x0 + 1,
            y0 + 1,
            x0 + self._CELL_WIDTH - 1,
            y0 + self._CELL_WIDTH - 1,
            width=2, outline="red", tags="cursor")


class GameView(tk.Tk):
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
        self.geometry("1000x1000")
