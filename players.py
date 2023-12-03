"""import rugbymen"""
from actions import *
import cards


class Player:
    def __init__(self, color):
        self._unplaced_rugbymen = [rugbymen.Rugbyman(color), 
                              rugbymen.Rugbyman(color), 
                              rugbymen.StrongRugbyman(color), 
                              rugbymen.HardRugbyman(color), 
                              rugbymen.SmartRugbyman(color), 
                              rugbymen.FastRugbyman(color)
                              ]
        self._rugbymen = []
        self._cards = [cards.ONE,
                        cards.TWO, 
                        cards.THREE, 
                        cards.FOUR, 
                        cards.FIVE, 
                        cards.SIX
                        ]
        self._color = color

    def color(self):
        return self._color
    
    def rugbymen(self):
        return self._rugbymen

    def input_select_rugbyman(self, game):
        rugbyman_selected = None
        while rugbyman_selected is None:
            input_x = input("Choose the x coordinate of the rugbyman you want to select")
            input_y = input("Choose the y coordinate of the rugbyman you want to select")
            for rugbyman in self._rugbymen:
                if rugbyman.posx() == input_x and rugbyman.posy() == input_y:
                    return rugbyman

    def available_actions(self, rugbyman, game):
        available = []
        if available_move_positions(rugbyman.posx(), rugbyman.posy(), rugbyman.scope(), game) != []: #définir rugbyman.scope()
            available.append(Actions.MOVE)
            print("To move a player, write "+ Actions.MOVE)
        if available_pass_positions(self.color(), rugbyman.posx(), rugbyman.posy(), rugbyman.pass_scope(), game) != []: #définir rugbyman.pass_scope()
            available.append(Actions.PASS)
            print("To pass the ball to a player, write "+ Actions.PASS)
        if available_tackle_positions(self.color(), rugbyman.posx(), rugbyman.posy(), rugbyman.tackle_scope(), game) != []: #définir rugbyman.tackle_scope()
            available.append(Actions.TACKLE)
            print("To tackle a player, write "+ Actions.TACKLE)
        if available_forward_pass(self.color(), rugbyman.posx(), rugbyman.posy(), rugbyman.forward_pass_scope(), game) != []: #définir rugbyman.forward_pass_scope()
            available.append(Actions.FORWARD)
            print("To realize a forward pass, write " + Actions.FORWARD)
        if available_score(self.color(), rugbyman.posx(), game) != []:
            available.append(Actions.SCORE)
            print("To score a try, write " + Actions.SCORE)

    def input_action(self, rugbyman, game):
        available = self.available_actions(rugbyman, game)
        while True:
            chosen_action = input("Choose your action:")
            if chosen_action == Actions.MOVE and Actions.MOVE in available:
                return move_rugbyman(rugbyman, game, moves_executed)
            if chosen_action == Actions.PASS and ACTIONS.PASS in available:
                return pass_ball(rugbyman, game, pass_scope)
            if chosen_action == Actions.TACKLE and Actions.TACKLE in available:
                return tackle(rugbyman, game)
            if chosen_action == Actions.FORWARD and Actions.Forward in available:
                return forward_pass(rugbyman, game) #ne pas oublier rugbyman.has_partners_in_front()
            if chosen_action == Actions.SCORE and Actions.SCORE in available:
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
                        self._cards = [cards.ONE,
                                    cards.TWO, 
                                    cards.THREE, 
                                    cards.FOUR, 
                                    cards.FIVE, 
                                    cards.SIX]
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
