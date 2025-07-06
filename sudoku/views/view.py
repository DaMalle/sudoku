import tkinter as tk


class MenuPage(tk.Frame):
    def __init__(self, root: tk.Frame | tk.Tk) -> None:
        super().__init__()
        self.root = root
        self._draw_buttons()

    def _draw_buttons(self) -> None:
        for difficulty in ["Easy", "Normal", "Hard"]:
            DifficultyButton(self, name=difficulty).pack()


class DifficultyButton(tk.Button):
    def __init__(self, root: tk.Frame | tk.Tk, name: str) -> None:
        super().__init__()
        self.root = root
        self.name = name

        self._configure_settings()

    def _configure_settings(self) -> None:
        self["text"] = self.name
        self["command"] = lambda: print(self.name)



root = tk.Tk()
root.geometry("100x100")

MenuPage(root).pack()

root.mainloop()
