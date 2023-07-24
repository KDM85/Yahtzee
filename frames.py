from widgets import *
from settings import *
from hand import Hand
import random


class Top_Frame(Frame):
    def __init__(self, parent: object):
        super().__init__(parent, 0, 0, 1, 0.2)
        self.parent = parent
        self.rolls_remaining = 3
        self.bonus_possible = False

        self.rolls_label = Label(self, "Rolls Remaining: " + str(self.rolls_remaining))
        self.high_score_label = Label(self, "High Score: ")
        self.roll_button = Button(self, "Roll", self.roll_dice)
        self.submit_button = Button(self, "Submit Hand", self.submit)
        self.submit_button.configure(state="disabled")

        self.build_dice()

        self.rolls_label.place(relx=0, rely=0, relwidth=0.5, relheight=0.2)
        self.high_score_label.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.2)
        self.roll_button.place(relx=0.02, rely=0.82, relwidth=0.48, relheight=0.18)
        self.submit_button.place(relx=0.52, rely=0.82, relwidth=0.46, relheight=0.18)

    def build_dice(self):
        for i in range(5):
            dice = Dice(self, i)
            dice.place(relx=(i / 5), rely=0.2, relwidth=0.2, relheight=0.6)
            setattr(self, "dice" + str(i), dice)

    def roll_dice(self):
        if self.roll_button.cget("text") == "Restart":
            return self.game_over()

        global HAND
        if self.rolls_remaining == 1:
            self.roll_button.configure(state="disabled")
        for i in range(5):
            if SELECTED_DICE[i] == "":
                HAND[i] = random.randint(1, 6)
                getattr(self, "dice" + str(i)).configure(text=str(HAND[i]))
        self.rolls_remaining -= 1
        self.rolls_label.configure(text="Rolls Remaining: " + str(self.rolls_remaining))
        self.submit_button.configure(state="normal")

    def submit(self):
        self.hand = Hand(SELECTED_OPTION, HAND)
        if SELECTED_OPTION == "yahtzee_bonus" and not self.hand.yahtzee():
            return

        self.submit_button.configure(state="disabled")
        temp = self.parent.bottom_frame.yahtzee_bonus_label.cget("text")
        getattr(self.parent.bottom_frame, SELECTED_OPTION + "_label").configure(
            text=str(self.hand.score())
        )
        getattr(self.parent.bottom_frame, SELECTED_OPTION).configure(state="disabled")
        if self.hand.yahtzee():
            self.bonus_possible = True
        if self.bonus_possible:
            self.parent.bottom_frame.yahtzee_bonus.configure(state="normal")
        if (
            self.parent.bottom_frame.check_upper()
            and self.parent.bottom_frame.check_lower()
        ):
            self.roll_button.configure(text="Restart", state="normal")
            self.submit_button.configure(state="disabled")
            score = int(self.parent.bottom_frame.total_score_label.cget("text"))
            if score > self.parent.high_score:
                self.parent.high_score = score
            self.high_score_label.configure(
                text="High Score: " + str(self.parent.high_score)
            )

        getattr(self.parent.bottom_frame, SELECTED_OPTION).configure(state="disabled")
        if SELECTED_OPTION == "yahtzee_bonus":
            if temp != "":
                self.parent.bottom_frame.yahtzee_bonus_label.configure(
                    text=str(self.hand.score() + int(temp))
                )
            self.parent.bottom_frame.yahtzee_bonus.configure(state="normal")
        self.reset()

    def highlight(self, die: int):
        global SELECTED_DICE
        if 0 in HAND:
            return
        if SELECTED_DICE[die] == "":
            SELECTED_DICE[die] = "x"
            getattr(self, "dice" + str(die)).configure(
                border_color="orangered", fg_color="tan1"
            )
        else:
            SELECTED_DICE[die] = ""
            getattr(self, "dice" + str(die)).configure(
                border_color="#202020", fg_color="white"
            )

    def reset(self):
        global HAND
        for i in range(5):
            HAND[i] = 0
            SELECTED_DICE[i] = ""
            getattr(self, "dice" + str(i)).configure(
                text="", fg_color="white", border_color="#202020"
            )
        self.rolls_remaining = 3
        self.rolls_label.configure(text="Rolls Remaining: " + str(self.rolls_remaining))
        self.parent.bottom_frame.highlight_option("")
        self.roll_button.configure(state="normal")

    def game_over(self):
        self.submit_button.configure(state="normal")
        self.bonus_possible = False
        for key in list(OPTIONS.keys()):
            if key in [
                "upper_score",
                "upper_bonus",
                "upper_total",
                "yahtzee_bonus",
                "lower_total",
                "upper_total2",
                "total_score",
            ]:
                state = "disabled"
            else:
                state = "normal"
            getattr(self.parent.bottom_frame, key + "_label").configure(text="")
            getattr(self.parent.bottom_frame, key).configure(state=state)
            self.roll_button.configure(text="Roll")


class Botton_Frame(Frame):
    def __init__(self, parent: object):
        super().__init__(parent, 0, 0.2, 1, 0.8)

        self.build_options()

    def build_options(self):
        i = 0
        for key, value in OPTIONS.items():
            if key in [
                "upper_score",
                "upper_bonus",
                "upper_total",
                "yahtzee_bonus",
                "lower_total",
                "upper_total2",
                "total_score",
            ]:
                state = "disabled"
            else:
                state = "normal"
            option = Option(self, key, value, state)
            option.place(relx=0, rely=i * 0.05, relwidth=0.5, relheight=0.05)
            setattr(self, key, option)
            label = Label(self, "")
            label.place(relx=0.5, rely=i * 0.05, relwidth=0.5, relheight=0.05)
            setattr(self, key + "_label", label)
            i += 1

    def highlight_option(self, option: str):
        global SELECTED_OPTION
        SELECTED_OPTION = option
        for key in list(OPTIONS.keys()):
            if key == option:
                getattr(self, key).configure(fg_color="orangered")
            else:
                getattr(self, key).configure(fg_color="#202020")

    def check_upper(self) -> bool:
        total = 0
        for key in ["aces", "twos", "threes", "fours", "fives", "sixes"]:
            if getattr(self, key + "_label").cget("text") == "":
                return False
            total += int(getattr(self, key + "_label").cget("text"))
        self.upper_score_label.configure(text=str(total))
        bonus = 35 if total >= 63 else 0
        self.upper_bonus_label.configure(text=bonus)
        self.upper_total_label.configure(text=str(total + bonus))
        return True

    def check_lower(self) -> bool:
        total = 0
        bonus = 0
        for key in [
            "three_of_a_kind",
            "four_of_a_kind",
            "full_house",
            "small_straight",
            "large_straight",
            "yahtzee",
            "chance",
        ]:
            if getattr(self, key + "_label").cget("text") == "":
                return False
            total += int(getattr(self, key + "_label").cget("text"))
            if self.yahtzee_bonus_label.cget("text") != "":
                bonus = int(self.yahtzee_bonus_label.cget("text"))
        self.lower_total_label.configure(text=str(total + bonus))
        upper_total = self.upper_total_label.cget("text")
        self.upper_total2_label.configure(text=upper_total)
        self.total_score_label.configure(text=total + bonus + int(upper_total))
        return True
