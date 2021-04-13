#!/usr/bin/env python3

#----------------------------------------------------------------------
# blackjack.py
# Jessica Harris
# 10/14/2018
#----------------------------------------------------------------------

from graphics import *
from CardDeck import *

#----------------------------------------------------------------------

def drawCard(filename: str, x: int, y: int, window: GraphWin):

    """draw image specified by filename centered at (x, y) in window"""

    p = Point(x, y)
    prefixes = ['cardset/', '../cardset/', './']
    for prefix in prefixes:
        fname = '{}{}'.format(prefix, filename)
        try:
            image = Image(p, fname)
            image.draw(window)
            return image
        except:
            pass

#----------------------------------------------------------------------

def cardInfo(cardNumber) -> (int, str):

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
    c for clubs, s for spades, h for hearts, d for diaomnds"""

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

#----------------------------------------------------------------------

def dealPlayerCards(totalPlayerCards, win, deck, totalPlayerValue, totalToDraw, totalValueDealer, totalCardsDealer,
                    totalDealerToDraw, ace, aceToDraw, aceCardNumber, aceToDrawDealer, aceDealer, aceCardDealer):

    #deal the card if user clicks the hit box
    hit = win.getMouse()
    xHit = hit.getX()
    yHit = hit.getY()
    while (600 <= xHit <= 700) and (200 <= yHit <= 250):
        totalToDraw.undraw()
        card = deck.dealOne()
        value, filename = cardInfo(card)
        totalPlayerCards += 1
        drawCard(filename, 100 * totalPlayerCards, 100, win)

        #check if it's an ace
        if value == 11:
            ace += 1
            aceCardNumber = totalPlayerCards
            aceToDraw = Text(Point(100 * totalPlayerCards, 175), "11")
            aceToDraw.draw(win)
            totalPlayerValue += 11
            totalToDraw = Text(Point(100, 200), f"Total: {totalPlayerValue}")
            totalToDraw.draw(win)
        else:
            valueToDraw = Text(Point(100 * totalPlayerCards, 175), value)
            valueToDraw.draw(win)
            totalPlayerValue += value
            totalToDraw = Text(Point(100, 200), f"Total: {totalPlayerValue}")
            totalToDraw.draw(win)

        #if the player busts and there's an ace, change the value to 1
        while totalPlayerValue > 21 and ace >= 1:
            totalPlayerValue -= 11
            totalPlayerValue += 1
            totalToDraw.undraw()
            totalToDraw = Text(Point(100, 200), f"Total: {totalPlayerValue}")
            totalToDraw.draw(win)
            ace -= 1
            aceToDraw.undraw()
            aceToDraw = Text(Point(100 * aceCardNumber, 175), "1")
            aceToDraw.draw(win)

        #if the player busts and there is no ace, end the game
        if totalPlayerValue > 21:
            bust = Text(Point(100, 225), "Busted!")
            bust.draw(win)
            return "Dealer"

        #check if Hit box is clicked
        hit = win.getMouse()
        xHit = hit.getX()
        yHit = hit.getY()

    #onto the dealer's cards if the player hasn't busted
    whoWins = dealDealersCards(deck, win, totalValueDealer, totalCardsDealer, totalDealerToDraw, totalPlayerValue, aceToDrawDealer, aceDealer,
                               aceCardDealer)
    return whoWins

#----------------------------------------------------------------------

def dealDealersCards(deck, win, totalValue, totalCards, totalToDraw, totalPlayerValue, aceToDraw, ace, aceCardNumber):

    #deal card until the dealer has a total of 17
    while totalValue < 17:
        totalToDraw.undraw()
        card = deck.dealOne()
        totalCards += 1
        value, filename = cardInfo(card)
        drawCard(filename, 100 * totalCards, 400, win)

        #check if it's an ace
        if value == 11:
            aceToDraw = Text(Point(100 * totalCards, 475), 11)
            aceToDraw.draw(win)
            ace += 1
            aceCardNumber = totalCards
        else:
            valueToDraw = Text(Point(100 * totalCards, 475), value)
            valueToDraw.draw(win)

        #increment and draw total
        totalValue += value
        totalToDraw = Text(Point(100, 500), f"Total: {totalValue}")
        totalToDraw.draw(win)

        #if the dealer busts and has an ace, change it's value to 1
        while totalValue > 21 and ace >= 1:
            aceToDraw.undraw()
            totalToDraw.undraw()
            ace -= 1
            totalValue -= 11
            totalValue += 1
            totalToDraw = Text(Point(100, 500), f"Total: {totalValue}")
            totalToDraw.draw(win)
            aceToDraw = Text(Point(100 * aceCardNumber, 475), 1)
            aceToDraw.draw(win)

        #if the dealer busts with no ace, end the game
        if totalValue >21:
            bust = Text(Point(100, 525), "Busted!")
            bust.draw(win)
            return "Player"

    #Check to see who won and end the game
    if totalPlayerValue < totalValue:
        return "Dealer"
    elif totalPlayerValue > totalValue:
        return "Player"
    else:
        return "Tie"

#----------------------------------------------------------------------

def main():
    # create window, card deck and shuffle it
    win = GraphWin('Blackjack', 800, 600)
    deck = CardDeck()
    deck.shuffle()

    # initialize some variables
    ace = 0
    aceCardNumber = 0
    aceToDraw = 0
    aceDealer = 0
    aceToDrawDealer = 0
    aceCardDealer = 0

    # Tell whose card is whose
    yourCards = Text(Point(50, 10), "Your Cards:")
    yourCards.draw(win)
    dealerCards = Text(Point(70, 325), "Dealer's Cards:")
    dealerCards.draw(win)

    #create the Hit button
    hitButton = Rectangle(Point(600, 200), Point(700, 250))
    hitButton.setFill("orange")
    hitButton.draw(win)
    hit = Text(Point(650, 225), "Hit")
    hit.draw(win)

    # deal the first card to the player and display it
    card = deck.dealOne()
    value, filename = cardInfo(card)
    drawCard(filename, 100, 100, win)

    #check if it's an ace
    if value == 11:
        ace += 1
        aceCardNumber = 1
        aceToDraw = Text(Point(100, 175), "11")
        aceToDraw.draw(win)
    else:
        valueToDraw = Text(Point(100, 175), value)
        valueToDraw.draw(win)

    #increment some variables
    totalCards = 1
    totalValuePlayer = value

    # deal second card to the player and display it
    card = deck.dealOne()
    value, filename = cardInfo(card)
    drawCard(filename, 200, 100, win)

    #check if it's an ace
    if value == 11:
        ace += 1
        aceCardNumber = 2
        aceToDraw = Text(Point(200, 175), 11)
        aceToDraw.draw(win)
    else:
        valueToDraw = Text(Point(200, 175), value)
        valueToDraw.draw(win)

    #increment and display the total
    totalCards += 1
    totalValuePlayer += value
    totalToDraw = Text(Point(100, 200), f"Total: {totalValuePlayer}")
    totalToDraw.draw(win)

    # if the player is dealt two aces, make one of them equal to 1
    if totalValuePlayer == 22:
        totalValuePlayer -= 11
        totalValuePlayer += 1
        ace -= 1
        aceToDraw.undraw()
        aceToDraw = Text(Point(200, 175), "1")
        aceToDraw.draw(win)
        totalToDraw.undraw()
        totalToDraw = Text(Point(100, 200), f"Total: {totalValuePlayer}")
        totalToDraw.draw(win)

    # deal the dealer's first card
    card = deck.dealOne()
    value, filename = cardInfo(card)
    drawCard(filename, 100, 400, win)
    totalCardsDealer = 1

    #check if it's an ace
    if value == 11:
        aceToDrawDealer = Text(Point(100, 475), value)
        aceToDrawDealer.draw(win)
        aceDealer += 1
        aceCardDealer = 1
    else:
        valueToDraw = Text(Point(100, 475), value)
        valueToDraw.draw(win)

    #increment and give total
    totalValueDealer = value
    totalDealerToDraw = Text(Point(100, 500), f"Total: {totalValueDealer}")
    totalDealerToDraw.draw(win)

    # determine who wins
    whoWins = dealPlayerCards(totalCards, win, deck, totalValuePlayer, totalToDraw, totalValueDealer, totalCardsDealer, totalDealerToDraw, ace,
                              aceToDraw, aceCardNumber, aceToDrawDealer, aceDealer, aceCardDealer)
    if whoWins == "Tie":
        whoWins = Text(Point(400, 300), f"It's a draw!")
    else:
        whoWins = Text(Point(400, 300), f"{whoWins} wins!")
    whoWins.draw(win)

    # wait for mouse click before closing window
    win.getMouse()
    win.close()
    
#----------------------------------------------------------------------

if __name__ == '__main__':
    main()