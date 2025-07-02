import sudoku.view
import sudoku.controller
import sudoku.model


def main():
    view = sudoku.view.GameView
    model = sudoku.model.SudokuModel
    controller = sudoku.controller.GameController(model, view)
    controller.start_game()


if __name__ == "__main__":
    main()
