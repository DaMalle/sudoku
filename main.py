from sudoku.views.view import MainView
from sudoku.controllers.controller import MainController
from sudoku.models.model import MainModel


def main():
    model = MainModel()
    view = MainView(model)
    controller = MainController(model, view)
    controller.start_game()


if __name__ == "__main__":
    main()
