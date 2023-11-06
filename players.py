import rugbymen
import actions

class Player:
    def __init__(self, rugbyman1, rugbyman2, strong_rugbyman, hard_rugbyman, smart_rugbyman, fast_rugbyman):
        self._unplaced_men = [rugbyman1, 
                              rugbyman2, 
                              strong_rugbyman, 
                              hard_rugbyman, 
                              smart_rugbyman, 
                              fast_rugbyman
                              ]
        self._cards = ["1","2","3","4","5","6"]

    def action(self):
        print("To move a player, write 1")
        print("To pass the ball to a player, write 2")
        print("To tackle a player, write 3")
        print("To realize a forward pass, write 4")
        print("To score a try, write 5")
        while True:
            chosen_action = input("Choose your action:")
            if chosen_action == "1":
                return move_player(self)
            if chosen_action == "2":
                return pass_ball(self)
            if chosen_action == "3":
                return tackle(self)
            if chosen_action == "4":
                return forward_pass(self)
            if chosen_action == "5":
                return score(self)

    def pick_card(self):
        """
        Discard the card chosen by the player and initialize the deck if all cards have been played
        """
        while True:
            picked_card = input("Which card do you pick ?")
            for i in range(len(self._cards)):
                if picked_card == self._cards[i]:
                    self._cards.pop(i)
                    if len(self._cards) == 0:
                        self._cards = ["1","2","3","4","5","6"]
                    return


class Ball:
    def __init__(self, init_position):
        self._position = init_position
        self._carrier = None
    
    def is_carried(self):
        return self._carrier != None
    
    def new_carrier(self, player):
        self._carrier = player
    
    def left(self):
        self._carrier = None

    def moved(self, position):
        self._position = position