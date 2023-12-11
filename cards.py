import enum
#Ne pas deplacer


def card_selected(deck, n_hit):
    value=convert_card_to_int(deck.pop(n_hit))
    if is_deck_empty(deck):
        deck = full_deck()
    return value

class Card(enum.Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"

    def get_image(self):
        if self == Card.ONE:
            return "Images/Carte1.png"
        if self == Card.TWO:
            return "Images/Carte2.png"
        if self == Card.THREE:
            return "Images/Carte3.png"
        if self == Card.FOUR:
            return "Images/Carte4.png"
        if self == Card.FIVE:
            return "Images/Carte5.png"
        if self == Card.SIX:
            return "Images/Carte6.png"
        raise ValueError("The card is not in the deck")



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

