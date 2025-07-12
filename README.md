# Sudoku Game in Python (Tkinter)

A simple Sudoku game built using Python's standard libraries, with a graphical user interface made in Tkinter.
---

## Project goal

To create a clean, self-contained Sudoku application that:
- Generates **valid Sudoku puzzles** with **only one solution**
- Provides an **interactive GUI** using Tkinter
- Has multiple difficulties (Easy, Normal, Hard and Expert)
- Uses keybinds or buttons on the GUI
- Able to start a new game without restarting the application
---

## Notes

- Puzzle solving are implemented using **backtracking**
- Games are created by:
  1. Creating solution
  2. Adding clues from the solution to an empty board
  3. Check if board has one solution by solving for multiple solutions
  4. If there are multiple solution, redo step 2 and 3.
- Safety measures has not been implemented for infeasible boards (fx too few clues)

---

## License

This project is released under the MIT License.
