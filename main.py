import customtkinter as ctk
from settings import *
from frames import *


class Game(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(TITLE)
        self._set_appearance_mode("Dark")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.minsize(WIDTH, HEIGHT)
        self.high_score = 0

        self.top_frame = Top_Frame(self)
        self.bottom_frame = Botton_Frame(self)


if __name__ == "__main__":
    game = Game()
    game.mainloop()
