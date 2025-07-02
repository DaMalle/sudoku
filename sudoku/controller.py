

class SudokuController:
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view


class GameController:
    def __init__(self, game_model, game_view) -> None:
        self.game_model = game_model
        self.game_view = game_view()

    def start_game(self) -> None:
        self._setup_keybinds()

        self.game_view.mainloop()

    def _setup_keybinds(self) -> None:
        root = self.game_view

        for i in range(1, 10, 1):
            root.bind(str(i), lambda _, number=i: self.handle_number_input(number))

        for key in ["<Up>", "w", "k"]:
            root.bind(key, lambda _: self.handle_move_cursor(0, -1))

        for key in ["<Down>", "s", "j"]:
            root.bind(key, lambda _: self.handle_move_cursor(0, 1))

        for key in ["<Left>", "a", "h"]:
            root.bind(key, lambda _: self.handle_move_cursor(-1, 0))

        for key in ["<Right>", "d", "l"]:
            root.bind(key, lambda _: self.handle_move_cursor(1, 0))

    def handle_number_input(self, number) -> None:
        """Handle number key press"""

        if self.game_model.is_game_active():
            selected_row, selected_column = self.game_view.get_selected_cell()
            if selected_row is not None and selected_column is not None:
                self.insert_number(selected_row, selected_column, number)

    def insert_number(self, x, y, number) -> None:
        """Process inserting a number into the selected cell"""

        if self.game_model.is_valid_insertion(x, y, number):
            self.game_model.insert_number(x, y, number)
            self.game_view.update_board()

            if self.game_model.is_complete():
                self.game_view.show_win_page()

    def handle_move_cursor(self, x_delta: int, y_delta: int) -> None:
        """Handle arrow key navigation"""

        current_row, current_column = self.game_view.board.get_selected_cell()
        if current_row is not None and current_column is not None:
            upper = 8 # upper index bound
            lower = 0 # lower index bound

            new_row = max(lower, min(upper, current_row + x_delta))
            new_column = max(lower, min(upper, current_column + y_delta))

            self.game_view.board.draw_cursor(new_row, new_column)


class MenuController:
    def __Init__(self) -> None:
        self.game_levels = ["easy", "normal", "hard"]
        self.default_level = "normal"
