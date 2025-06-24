

class SudokuController:
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view


class GameController:
    def __Init__(self, game_model, game_view) -> None:
        self.game_model = game_model
        self.game_view = game_view

    def _setup_keybinds(self) -> None:
        root = self.game_view.root

        for i in range(1, 10, 1):
            root.bind(str(i), lambda _, number=i: self.handle_number_input(number))

    def handle_number_input(self, number) -> None:
        """Handle number key press"""

        if self.game_model.is_game_active():
            selected_row, selected_column = self.game_view.get_selected_cell()
            if selected_row is not None and selected_column is not None:
                self.process_insert_number(selected_row, selected_column, number)


    def handle_move_navigation(self, row_delta: int, column_delta: int) -> None:
        """Handle arrow key navigation"""

        current_row, current_column = self.game_view.get_selected_cell()
        if current_row is not None and current_column is not None:
            upper = 8 # upper index bound
            lower = 0 # lower index bound

            new_row = max(lower, min(upper, current_row + row_delta))
            new_column = max(lower, min(upper, current_column + column_delta))

            self.game_view.update_selected_cell(new_row, new_column)

    def process_insert_number(self, row, column, number) -> None:
        """Process inserting a number into the selected cell"""

        if self.game_model.is_valid_insertion(row, column, number):
            self.game_model.insert_number(row, column, number)
            self.game_view.update_board()

            if self.game_model.is_complete():
                self.game_view.show_win_page()

class MenuController:
    def __Init__(self) -> None:
        pass
