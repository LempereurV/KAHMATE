import rugbymen
from actions import *
from cards import Card
from actions import Action

class Player:
    def __init__(self, color):
        # Commentaires suivants à evaluer je pense que les unplaces rugbymen ne servent à rien
        """
        self._unplaced_rugbymen = [
            rugbymen.Rugbyman(color),
            rugbymen.Rugbyman(color),
            rugbymen.StrongRugbyman(color),
            rugbymen.HardRugbyman(color),
            rugbymen.SmartRugbyman(color),
            rugbymen.FastRugbyman(color),
        ]
        """
        # Liste qui est je pense à interpréter comme la liste des rugbymen que le joueur choisi de jouer (au maxmimum 2)
        self._rugbymen = []
        self._cards = [Card.ONE, Card.TWO, Card.THREE, Card.FOUR, Card.FIVE, Card.SIX]
        self._color = color
        self.can_play = True

    def can_play(self):
        return self.can_play

    def choose_rugbymen(self, rugbyman):
        """
        Choose the rugbymen that the player wants to play with
        """
        if len(self._rugbymen) == 2:
            print("You already have two rugbyman, you can't select another one")
        else:
            if rugbyman in self.show_rugbymen():
                if rugbymen.Rugbyman.spec(rugbyman) == rugbymen.Spec.NORMAL:
                    # There is two normal rugbymen on the board we have to make sure we dont select the same one twice
                    if rugbymen.Rugbyman.pos(rugbyman) == rugbymen.Rugbyman.pos(
                        self.show_rugbyman(0)
                    ):
                        self.add_rugbyman(rugbyman)
                        return True
                else:
                    print("You have already selected this rugbyman")
            else:
                self.add_rugbyman(rugbyman)
                return True
        return False

    def reset_player(self):
        self._rugbymen = []
        #self._cards = [Card.ONE, Card.TWO, Card.THREE, Card.FOUR, Card.FIVE, Card.SIX]
        self.can_play = True

    def set_can_play(self, boolean):
        self.can_play = boolean

    def n_rugbymen(self):
        return len(self._rugbymen)

    def actualize_can_play(self):
        if self.n_rugbymen() == 2:
            move_points = 0
            for rugbyman in self.show_rugbymen():
                move_points += rugbymen.Rugbyman.move_left(rugbyman)
                #print(move_points)
            if move_points == 0:
                self.set_can_play(False)

    def color(self):
        return self._color

    def rugbymen(self):
        return self._rugbymen
    
    def number_of_rugbymen(self):
        return len(self._rugbymen)
    # plural
    def show_rugbymen(self):
        return self._rugbymen

    # singular
    def show_rugbyman(self, i):
        return self._rugbymen[i]

    def add_rugbyman(self, rugbyman):
        self._rugbymen.append(rugbyman)

    def available_actions(self, rugbyman, game):
        available = []
        if available_move_positions(rugbyman.posx(), rugbyman.posy(), rugbyman.moves_left(), game) != []:
            available.append(Action.MOVE)
            print("To move a player, write " + Action.MOVE)
        if available_pass_positions(self.color(), rugbyman.posx(), rugbyman.posy(), rugbyman.pass_scope(), game) != []: #définir rugbyman.pass_scope()
            available.append(Action.PASS)
            print("To pass the ball to a player, write " + Action.PASS)
        if available_tackle_positions(self.color(), rugbyman.posx(), rugbyman.posy(), rugbyman.tackle_scope(), game) != []: #définir rugbyman.tackle_scope()
            available.append(Action.TACKLE)
            print("To tackle a player, write " + Action.TACKLE)
        if available_forward_pass(self.color(), rugbyman.posx(), rugbyman.posy(), rugbyman.forward_pass_scope(), game) != []: #définir rugbyman.forward_pass_scope()
            available.append(Action.FORWARD_PASS)
            print("To realize a forward pass, write " + Action.FORWARD_PASS)
        if available_score(self.color(), rugbyman.posx(), game) != []:
            available.append(Action.SCORE)
            print("To score a try, write " + Action.SCORE)

    def input_action(self, rugbyman, game):
        available = self.available_actions(rugbyman, game)
        while True:
            chosen_action = input("Choose your action:")
            if chosen_action == "1" and 1 in available:
                return move_rugbyman(rugbyman, game, moves_executed)
            if chosen_action == "2" and 2 in available:
                return pass_ball(rugbyman, game, pass_scope)
            if chosen_action == "3" and 3 in available:
                return tackle(rugbyman, game)
            if chosen_action == "4" and 4 in available:
                return forward_pass(
                    rugbyman, game
                )  # ne pas oublier rugbyman.has_partners_in_front()
            if chosen_action == "5" and 5 in available:
                return score(rugbyman, game)

    def place_rugbyman(self):
        try:
            rugbyman = self._unplaced_rugbymen.pop()
            pass
        except IndexError:
            raise ("No rugbyman to place")

    def pick_card(self):
        """
        Discard the card chosen by the player and reinitialize the deck if all cards have been played
        """
        while True:
            picked_card = input("Which card do you pick ?")
            for i in range(len(self._cards)):
                if picked_card == self._cards[i]:
                    self._cards.pop(i)
                    if len(self._cards) == 0:
                        self._cards = [
                            Card.ONE,
                            Card.TWO,
                            Card.THREE,
                            Card.FOUR,
                            Card.FIVE,
                            Card.SIX,
                        ]
                    return


class Ball:
    def __init__(self, init_position):
        self._position = init_position
        self._carrier = None

    def is_carried(self):
        return self._carrier != None

    def new_carrier(self, player):
        self._carrier = player

    def is_carried_by_rugbyman(self, rugbyman):
        return self.is_carried() and self._carrier() == rugbyman

    def left(self):
        self._carrier = None

    def moved(self, position):
        self._position = position
