from sudoku.views.interfaces import IBoardView, IMainView


class MainController:
    def __init__(self, model, view: IMainView) -> None:
        self.model = model
        self.view: IMainView = view
        self.board_view: IBoardView = self.view.board

    def start_game(self) -> None:
        self._setup_keybinds()

        self.view.run()

    def _setup_keybinds(self) -> None:
        root = self.view

        for key in range(1, 10, 1):
            root.bind_key(
                str(key), lambda _: self.handle_number_input(key)
            )

        root.bind_key("<Up>", lambda _: self.handle_move_cursor(0, -1))
        root.bind_key("<Down>", lambda _: self.handle_move_cursor(0, 1))
        root.bind_key("<Left>", lambda _: self.handle_move_cursor(-1, 0))
        root.bind_key("<Right>", lambda _: self.handle_move_cursor(1, 0))

    def handle_number_input(self, number: int) -> None:
        """Handle number key press"""

        selected_x, selected_y = self.board_view.get_cursor()
        if selected_x is not None and selected_y is not None:
            self.insert_number(selected_x, selected_y, number)

    def insert_number(self, x: int, y: int, number: int) -> None:
        """Process inserting a number into the selected cell"""

        self.model.board[y][x].current = number
        self.board_view.update_board()

        if self.model.is_complete():
            self.view.show_win_page()

    def handle_move_cursor(self, x_delta: int, y_delta: int) -> None:
        """Handle arrow key navigation"""

        current_row, current_column = self.board_view.get_cursor()
        if current_row is not None and current_column is not None:
            upper = 8 # upper index bound
            lower = 0 # lower index bound

            new_row = max(lower, min(upper, current_row + x_delta))
            new_column = max(lower, min(upper, current_column + y_delta))

            self.board_view.update_cursor(new_row, new_column)
