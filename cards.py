import enum


class Card(enum.Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"


def full_deck():
    return [
        Card.ONE,
        Card.TWO,
        Card.THREE,
        Card.FOUR,
        Card.FIVE,
        Card.SIX
    ]

def discard_card(card, deck):
    """
    Discard the card chosen by the player and reinitialize the deck if all cards have been played
    """
    for i in range(len(deck)):
        if card == deck[i]:
            deck.pop(i)
            if len(deck) == 0:
                deck = full_deck()
            return deck
    raise ValueError("The card is not in the deck")

def is_deck_empty(deck):
    return len(deck) == 0

def is_card_in_deck(card, deck):
    for i in range(len(deck)):
        if card == deck[i]:
            return True
    return False


def convert_int_to_card(card):
    if card == 1:
        return Card.ONE
    if card == 2:
        return Card.TWO
    if card == 3:
        return Card.THREE
    if card == 4:
        return Card.FOUR
    if card == 5:
        return Card.FIVE
    if card == 6:
        return Card.SIX
    raise ValueError("The card is not in the deck")

def convert_card_to_int(card):
    if card == Card.ONE:
        return 1
    if card == Card.TWO:
        return 2
    if card == Card.THREE:
        return 3
    if card == Card.FOUR:
        return 4
    if card == Card.FIVE:
        return 5
    if card == Card.SIX:
        return 6
    raise ValueError("The card is not in the deck")