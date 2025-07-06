import sudoku.view
import sudoku.controller
import sudoku.model


def main():
    model = sudoku.model.MainModel()
    view = sudoku.view.MainView(model)
    controller = sudoku.controller.GameController(model, view)
    controller.start_game()


if __name__ == "__main__":
    main()
