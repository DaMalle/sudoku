class MainController:
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

    def start_game(self) -> None:
        self._setup_keybinds()

        self.view.run()

    def _setup_keybinds(self) -> None:
        root = self.view

        for key in range(1, 10, 1):
            root.bind(
                str(key), lambda _: self.handle_number_input(key)
            )

        root.bind("<Up>", lambda _: self.handle_move_cursor(0, -1))
        root.bind("<Down>", lambda _: self.handle_move_cursor(0, 1))
        root.bind("<Left>", lambda _: self.handle_move_cursor(-1, 0))
        root.bind("<Right>", lambda _: self.handle_move_cursor(1, 0))

    def handle_number_input(self, number: int) -> None:
        """Handle number key press"""

        if self.model.is_active():
            selected_x, selected_y = self.view.get_selected_cell()
            if selected_x is not None and selected_y is not None:
                self.insert_number(selected_x, selected_y, number)

    def insert_number(self, x: int, y: int, number: int) -> None:
        """Process inserting a number into the selected cell"""

        if self.model.is_valid_insertion(x, y, number):
            self.model.insert_number(x, y, number)
            self.view.update_board()

            if self.model.is_complete():
                self.view.show_win_page()

    def handle_move_cursor(self, x_delta: int, y_delta: int) -> None:
        """Handle arrow key navigation"""

        current_row, current_column = self.view.board.get_cursor()
        if current_row is not None and current_column is not None:
            upper = 8 # upper index bound
            lower = 0 # lower index bound

            new_row = max(lower, min(upper, current_row + x_delta))
            new_column = max(lower, min(upper, current_column + y_delta))

            self.view.board.update_cursor(new_row, new_column)


class MenuController:
    def __Init__(self) -> None:
        self.levels = ["easy", "normal", "hard"]
        self.default_level = "normal"
