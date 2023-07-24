class Hand:
    def __init__(self, option: str, hand: list):
        self.option = option
        self.hand = hand

    def singles(self, dice: int) -> int:
        count = self.hand.count(dice)
        return count * dice

    def three_of_a_kind(self) -> bool:
        for dice in self.hand:
            if self.hand.count(dice) >= 3:
                return True
        return False

    def four_of_a_kind(self) -> bool:
        for dice in self.hand:
            if self.hand.count(dice) >= 4:
                return True
        return False

    def full_house(self) -> bool:
        unique_numbers = []
        count = 0
        for dice in self.hand:
            if dice not in unique_numbers:
                count += 1
                unique_numbers.append(dice)
        return count == 2

    def small_straight(self) -> bool:
        self.hand.sort()
        lowest = self.hand[0]
        highest = self.hand[4]
        return (
            lowest + 1 in self.hand
            and lowest + 2 in self.hand
            and lowest + 3 in self.hand
        ) or (
            highest - 1 in self.hand
            and highest - 2 in self.hand
            and highest - 3 in self.hand
        )

    def large_straight(self) -> bool:
        self.hand.sort()
        lowest = self.hand[0]
        highest = self.hand[4]
        return self.small_straight() and (
            lowest + 4 in self.hand or highest - 4 in self.hand
        )

    def yahtzee(self) -> bool:
        for dice in self.hand:
            if self.hand.count(dice) == 5:
                return True
        return False

    def dice_total(self) -> int:
        total = 0
        for dice in self.hand:
            total += dice
        return total

    def score(self) -> int:
        match self.option:
            case "aces":
                return self.singles(1)
            case "twos":
                return self.singles(2)
            case "threes":
                return self.singles(3)
            case "fours":
                return self.singles(4)
            case "fives":
                return self.singles(5)
            case "sixes":
                return self.singles(6)
            case "three_of_a_kind":
                return self.dice_total() if self.three_of_a_kind() else 0
            case "four_of_a_kind":
                return self.dice_total() if self.four_of_a_kind() else 0
            case "full_house":
                return 25 if self.full_house() else 0
            case "small_straight":
                return 30 if self.small_straight() else 0
            case "large_straight":
                return 40 if self.large_straight() else 0
            case "yahtzee":
                return 50 if self.yahtzee() else 0
            case "yahtzee_bonus":
                return 100 if self.yahtzee() else 0
            case "chance":
                return self.dice_total()
