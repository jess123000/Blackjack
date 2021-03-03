import random

class CardDeck:

    def __init__(self):
        self.freshDeck()

    def freshDeck(self):
        # generally the constructor initializes all the instance variables
        # but we're calling this method from the constructor so we create the instance variables here
        self.cards = []
        self.position = 0

        for i in range(52):
            self.cards.append(i)

    def shuffle(self):
        random.shuffle(self.cards)

    def dealOne(self) -> int:
        if self.position < 52:
            card = self.cards[self.position]
            self.position += 1
            return card
        else:
            return None