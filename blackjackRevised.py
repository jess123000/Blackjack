#!/usr/bin/env python3

#----------------------------------------------------------------------
# blackjackRevised.py
# simply blackjack.py refactored to look nicer. Will eventually become blackjack.py
# Jessica Harris
# 10/14/2018
#----------------------------------------------------------------------

from __future__ import annotations
from graphics import *
from CardDeck import *

class Blackjack:
    def __init__(self, win: GraphWin, deck: CardDeck):
        self.win = win
        self.deck = deck
        self.deck.shuffle()
        self.hitButton = Rectangle(Point(600, 200), Point(700, 250))
        self.hitButton.setFill("orange")
        self.hitButton.draw(self.win)
        self.hitText = Text(Point(650, 225), "Hit")
        self.hitText.draw(self.win)
        self.yourCardsText = Text(Point(50, 10), "Your Cards:")
        self.yourCardsText.draw(self.win)
        self.dealerCardsText = Text(Point(70, 325), "Dealer's Cards:")
        self.dealerCardsText.draw(self.win)
        self.acePlayer = 0
        self.aceCardNumberPlayer = 0
        self.aceCardNumberDealer = 0
        self.aceToDrawPlayer = 0
        self.aceDealer = 0
        self.aceToDrawDealer = 0
        self.totalPlayerValue = 0
        self.totalPlayerCards = 0
        self.totalDealerCards = 0
        self.totalDealerValue = 0
        self.runGame()

    # ----------------------written by Dave Reed-----------------------

    def drawCard(self, filename: str, x: int, y: int):

        """draw image specified by filename centered at (x, y) in window"""

        p = Point(x, y)
        prefixes = ['cardset/', '../cardset/', './']
        for prefix in prefixes:
            fname = '{}{}'.format(prefix, filename)
            try:
                image = Image(p, fname)
                image.draw(self.win)
                return image
            except:
                pass

    # ----------------------written by Dave Reed-----------------------

    def cardInfo(self, cardNumber) -> (int, str):

        """returns the blackjack value and and filename for card specified
        by cardNumber

        0-12 are the Ace-King of clubs
        13-25 are the Ace-King of spades
        26-38 are the Ace-King of hearts
        39-51 are the Ace-King of diamonds

        the blackjack value for the cards 2-9 are the corresponding
        number; 10, Jack, Queen, and King all have blackjack values of 10
        and an Ace has a value of 11

        filename is of the form: ##s.gif
        where ## is a two digit number (leading 0 if less than 10)
        and s is a letter corresponding to the suit value
        c for clubs, s for spades, h for hearts, d for diamonds"""

        # calculate suit and face numbers
        suitNum = cardNumber // 13
        faceNum = cardNumber % 13

        # calculate blackjack value
        value = faceNum + 1
        if value > 10:
            value = 10
        elif value == 1:
            value = 11

        # calculate name of file
        # face is a number from 1 to 13 with leading zeros for 1-9
        suits = 'cshd'
        filename = '{:>02}{}.gif'.format(faceNum + 1, suits[suitNum])
        return value, filename

    # ----------------------------------------------------------------------

    def checkIfAce(self, value: int, dealerPlayer: str) -> None:
        # determine if dealer or player drew
        if dealerPlayer == "player":
            # check if it's an ace
            if value == 11:
                self.aceToDrawPlayer = Text(Point(100 * self.totalPlayerCards, 475), value)
                self.aceToDrawPlayer.draw(self.win)
                self.acePlayer += 1
                self.aceCardNumberPlayer = self.totalPlayerCards
            else:
                valueToDraw = Text(Point(100 * self.totalPlayerCards, 475), value)
                valueToDraw.draw(self.win)
        else:
            # check if it's an ace
            if value == 11:
                self.aceToDrawDealer = Text(Point(100 * self.totalDealerCards, 475), value)
                self.aceToDrawDealer.draw(self.win)
                self.aceDealer += 1
                self.aceCardNumberDealer = self.totalDealerCards
            else:
                valueToDraw = Text(Point(100 * self.totalDealerCards, 475), value)
                valueToDraw.draw(self.win)

    # ----------------------------------------------------------------------

    def aceToOne(self, dealerPlayer: str, totalToDraw) -> None:
        if dealerPlayer == "player":
            self.totalPlayerValue -= 11
            self.totalPlayerValue += 1
            totalToDraw.undraw()
            totalToDraw = Text(Point(100, 200), f"Total: {self.totalPlayerValue}")
            totalToDraw.draw(self.win)
            self.acePlayer -= 1
            self.aceToDrawPlayer.undraw()
            self.aceToDrawPlayer = Text(Point(100 * self.aceCardNumberPlayer, 175), "1")
            self.aceToDrawPlayer.draw(self.win)
        else:
            self.aceToDrawDealer.undraw()
            totalToDraw.undraw()
            self.aceDealer -= 1
            self.totalPlayerValue -= 11
            self.totalPlayerValue += 1
            totalToDraw = Text(Point(100, 500), f"Total: {self.totalPlayerValue}")
            totalToDraw.draw(self.win)
            self.aceToDrawDealer = Text(Point(100 * self.aceCardNumberDealer, 475), 1)
            self.aceToDrawDealer.draw(self.win)

    # ----------------------------------------------------------------------

    def dealPlayerCards(self, totalToDraw: Text) -> bool:

        # deal the card if user clicks the hit box
        hit = self.win.getMouse()
        xHit = hit.getX()
        yHit = hit.getY()
        while (600 <= xHit <= 700) and (200 <= yHit <= 250):
            totalToDraw.undraw()
            card = self.deck.dealOne()
            value, filename = self.cardInfo(card)
            self.totalPlayerCards += 1
            self.drawCard(filename, 100 * self.totalPlayerCards, 100)

            self.checkIfAce(value, "player")

            # if the player busts and there's an ace, change the value to 1
            while self.totalPlayerValue > 21 and self.acePlayer >= 1:
                self.aceToOne("player", totalToDraw)

            # if the player busts and there is no ace, dealer won
            if self.totalPlayerValue > 21:
                bust = Text(Point(100, 225), "Busted!")
                bust.draw(self.win)
                return True

            # check if Hit box is clicked
            hit = self.win.getMouse()
            xHit = hit.getX()
            yHit = hit.getY()

        # if player didn't bust, find who won normally
        return False

    # ----------------------------------------------------------------------

    def dealDealersCards(self, totalToDraw: Text) -> bool:

        # deal card until the dealer has a total of 17
        while self.totalPlayerValue < 17:
            totalToDraw.undraw()
            card = self.deck.dealOne()
            self.totalDealerCards += 1
            value, filename = self.cardInfo(card)
            self.drawCard(filename, 100 * self.totalDealerCards, 400)

            self.checkIfAce(value, "dealer")

            # increment and draw total
            self.totalPlayerValue += value
            totalToDraw = Text(Point(100, 500), f"Total: {self.totalPlayerValue}")
            totalToDraw.draw(self.win)

            # if the dealer busts and has an ace, change it's value to 1
            while self.totalPlayerValue > 21 and self.aceDealer >= 1:
                self.aceToOne("dealer", totalToDraw)

            # if the dealer busts with no ace, end the game
            if self.totalPlayerValue > 21:
                bust = Text(Point(100, 525), "Busted!")
                bust.draw(self.win)
                return True

        # if the dealer didn't bust, find who won normally
        return False

    # -----------------------------------------------------------------

    def runGame(self) -> None:
        # deal the first card to the player and display it
        card = self.deck.dealOne()
        value, filename = self.cardInfo(card)
        self.drawCard(filename, 100, 100)

        self.checkIfAce(value, "player")

        # increment some variables
        self.totalPlayerCards += 1
        self.totalPlayerValue += value

        # deal second card to the player and display it
        card = self.deck.dealOne()
        value, filename = self.cardInfo(card)
        self.drawCard(filename, 200, 100)
        self.checkIfAce(value, "player")

        # increment and display the total
        self.totalPlayerCards += 1
        self.totalPlayerValue += value
        totalToDraw = Text(Point(100, 200), f"Total: {self.totalPlayerValue}")
        totalToDraw.draw(self.win)

        # if the player is dealt two aces, make one of them equal to 1
        if self.totalPlayerValue == 22:
            self.aceToOne("player", totalToDraw)

        # deal the dealer's first card
        card = self.deck.dealOne()
        value, filename = self.cardInfo(card)
        self.drawCard(filename, 100, 400)
        self.totalDealerCards += 1
        self.checkIfAce(value, "dealer")

        # increment and give total
        self.totalDealerValue += value
        totalDealerToDraw = Text(Point(100, 500), f"Total: {self.totalDealerValue}")
        totalDealerToDraw.draw(self.win)

        dealerWins = self.dealPlayerCards(totalToDraw)
        playerWins = self.dealDealersCards(totalDealerToDraw)

        # determine who won
        if dealerWins:
            whoWins = Text(Point(400, 300), "Dealer wins!")
        elif playerWins:
            whoWins = Text(Point(400, 300), "Player wins!")
        elif self.totalDealerValue < self.totalPlayerValue:
            whoWins = Text(Point(400, 300), "Player wins!")
        elif self.totalDealerValue > self.totalPlayerValue:
            whoWins = Text(Point(400, 300), "Dealer wins!")
        else:
            whoWins = Text(Point(400, 300), f"It's a draw!")

        whoWins.draw(self.win)

        # wait for mouse click before closing window
        self.win.getMouse()
        self.win.close()

#----------------------------------------------------------------------

def main():
    # create the window, card deck, and start the game
    win = GraphWin("Blackjack", 800, 600)
    deck = CardDeck()
    Blackjack(win, deck)

#----------------------------------------------------------------------

if __name__ == '__main__':
    main()