import customtkinter as ctk
from settings import *


class Frame(ctk.CTkFrame):
    def __init__(
        self,
        parent: object,
        relx: float,
        rely: float,
        relwidth: float,
        relheight: float,
    ):
        super().__init__(parent)
        self.configure(fg_color="#202020")
        self.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)


class Label(ctk.CTkLabel):
    def __init__(self, parent: object, text: str):
        super().__init__(parent)
        self.configure(text=text, font=LABEL_FONT)


class Button(ctk.CTkButton):
    def __init__(self, parent: object, text: str, command: callable):
        super().__init__(parent)
        self.configure(
            text=text,
            font=BUTTON_FONT,
            corner_radius=25,
            fg_color="orangered",
            hover_color="chocolate1",
            command=command,
        )


class Dice(ctk.CTkButton):
    def __init__(self, parent: object, die: int):
        super().__init__(parent)
        self.parent = parent
        self.configure(
            width=(WIDTH - 50) / 5,
            height=(WIDTH - 50) / 5,
            border_width=2,
            border_color="#202020",
            corner_radius=40,
            text="",
            text_color="black",
            font=("Tahoma", 24, "bold"),
            fg_color="white",
            hover_color="chocolate1",
            command=lambda x=die: self.on_click(x),
        )

    def on_click(self, die: int):
        self.parent.highlight(die)


class Option(ctk.CTkButton):
    def __init__(self, parent: object, key: str, value: str, state: str):
        super().__init__(parent)
        self.parent = parent
        self.configure(
            width=WIDTH / 2,
            height=30,
            text=value,
            font=LABEL_FONT,
            fg_color="#202020",
            hover_color="chocolate1",
            corner_radius=15,
            state=state,
            command=lambda x=key: self.on_click(x),
        )

    def on_click(self, key):
        self.parent.highlight_option(key)
