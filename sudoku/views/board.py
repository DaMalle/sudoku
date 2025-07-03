import tkinter as tk


class Board(tk.Canvas):
    def __init__(self, root: tk.Tk | tk.Frame, board_model) -> None:
        super().__init__(root)
        self.root: tk.Tk | tk.Frame = root
        self.board_model = board_model

        self.cursor_x = 0
        self.cursor_y = 0

        self._MARGIN = 20
        self._CELL_WIDTH = 50
        self._GRID_WIDTH = 9 * self._CELL_WIDTH
        self._BOARD_WIDTH = self._MARGIN * 2 + self._GRID_WIDTH

        self._configure_widget()
        self._draw_puzzle(board_model)
        self._draw_grid_lines()
        self._draw_cursor(self.cursor_x, self.cursor_y)

    def get_cursor(self) -> tuple[int, int]:
        """Get cursor location (x, y)"""

        return (self.cursor_x, self.cursor_y)

    def update_cursor(self, x: int, y: int) -> None:
        self.delete("cursor") # delete old cursor if any
        self._draw_cursor(x=x, y=y)


    def _draw_cursor(self, x: int, y: int) -> None:
        """Draws a red square (cursor) at (x,y)"""

        # x0, y0 represents the top left corner of the cell x, y are in
        y0 = self._MARGIN + y * self._CELL_WIDTH
        x0 = self._MARGIN + x * self._CELL_WIDTH

        self.create_rectangle( # the 1's keep the rectangle within the cell boarder
            x0 + 1,
            y0 + 1,
            x0 + self._CELL_WIDTH - 1,
            y0 + self._CELL_WIDTH - 1,
            width=2, outline="red", tags="cursor"
        )
        self.cursor_x = x
        self.cursor_y = y

    def update_cell(self, x: int, y: int, number: int) -> None:
        self.delete(f"cell{x}{y}")

        self.create_text(
            x * self._CELL_WIDTH + self._MARGIN + self._CELL_WIDTH // 2,
            y * self._CELL_WIDTH + self._MARGIN + self._CELL_WIDTH // 2,
            text=number, tags=f"cell{x}{y}", font=("Arial", self._CELL_WIDTH // 4)
        )

    def _configure_widget(self) -> None:
        self["bg"] = "white"
        self["width"] = self._BOARD_WIDTH
        self["height"] = self._BOARD_WIDTH

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
            self._MARGIN + index * self._CELL_WIDTH,
            self._MARGIN,
            self._MARGIN + index * self._CELL_WIDTH,
            self._BOARD_WIDTH - self._MARGIN,
            fill=fill, width=width
        )

    def _draw_horizontal_line(self, index: int, fill: str, width: int) -> None:
        self.create_line(
            self._MARGIN,
            self._MARGIN + index * self._CELL_WIDTH,
            self._BOARD_WIDTH - self._MARGIN,
            self._MARGIN + index * self._CELL_WIDTH,
            fill=fill, width=width
        )

    def _draw_puzzle(self, board_model) -> None:
        for iy, row in enumerate(board_model):
            for ix, number in enumerate(row):
                self._draw_cell_number(ix, iy, number)

    def _draw_cell_number(self, x, y, number) -> None:
        if number != 0:
            self.create_text(
                # at the center:
                x * self._CELL_WIDTH + self._MARGIN + self._CELL_WIDTH // 2,
                y * self._CELL_WIDTH + self._MARGIN + self._CELL_WIDTH // 2,
                text=number, font=("Arial", self._CELL_WIDTH // 4)
            )
