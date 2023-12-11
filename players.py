import rugbymen
<<<<<<< HEAD
from actions import *
from cards import Card
import actions

=======
import actions
import cards
import players 
import game
import color
>>>>>>> branche_de_felix2

class Player:
    def __init__(self, color,Game,turn_color,Graphique):
        
        # Placement order of the rugbylen (mostly for the initialisation but can be usefull later)
        self._placement_order= actions.placement_orders(color)

        # List of all the rugbymen of the player
        self._rugbymen = actions.positions_rugbymen_player(self._placement_order, Graphique)

        # List of all the rugbymen chosen by the player for his turn 
        self._chosen_rugbymen = []


        self._deck=cards.full_deck()

        self._color = color
        if color == turn_color:
            self.can_play = True
        else:
            self.can_play = False

    ### A supprimer ###

    def get_color(self):
        return self._color
    
    ####

    def has_ball(self):
        """
        Return True if the player has the ball, False otherwise
        """
        for rugbyman in self.get_rugbymen():
            if rugbyman.has_ball():
                return True
        return False


    

    def add_choosen_rugbymen(self, rugbyman):
        """
        Choose the rugbymen that the player wants to play with
        """
        if len(self._chosen_rugbymen) == 2:
            print("You already have two rugbyman, you can't select another one")
        else:
            if rugbyman in self.get_chosen_rugbymen():
                if rugbymen.Rugbyman.spec(rugbyman) == rugbymen.Spec.NORMAL:
                    # There is two normal rugbymen on the board we have to make sure we dont select the same one twice
                    if rugbymen.Rugbyman.pos(rugbyman) == rugbymen.Rugbyman.pos(
                        self.get_chosen_rugbymen()[0]
                    ):
                        self.add_rugbyman(rugbyman)
                        return True
                else:
                    print("You have already selected this rugbyman")
            else:
                self.add_rugbyman(rugbyman)
                return True
        return False

<<<<<<< HEAD
    def reset_player(self):
        self._rugbymen = []
        # self._cards = [Card.ONE, Card.TWO, Card.THREE, Card.FOUR, Card.FIVE, Card.SIX]
=======
    def reset_player_after_turn(self):
        self._chosen_rugbymen = []
>>>>>>> branche_de_felix2
        self.can_play = True

    def get_can_play(self):
        return self.can_play
    
    def set_can_play(self, boolean):
        self.can_play = boolean

    def actualize_can_play(self):
        cond=False
        if self.get_deck()==[]:
            self.refresh_deck()
        if self.get_n_rugbymen() >= 2:
            move_points = 0
            for rugbyman in self.get_chosen_rugbymen():
                if (rugbyman.get_KO()==0 
                    and (rugbymen.Rugbyman.move_left(rugbyman)>0
                         or rugbyman.has_ball())):
                    cond=True
                move_points += rugbymen.Rugbyman.move_left(rugbyman)
<<<<<<< HEAD
                # print(move_points)
            if move_points == 0:
=======
            if not cond:
>>>>>>> branche_de_felix2
                self.set_can_play(False)
            else :
                if move_points == 0 :
                    if self.has_ball():
                        print("You can only pass the ball")
                    else:
                        self.set_can_play(False)

    def color(self):
        return self._color

    def get_chosen_rugbymen(self):
        return self._chosen_rugbymen
    
    def get_n_rugbymen(self):
        return len(self._chosen_rugbymen)

    def get_rugbymen(self):
        return self._rugbymen
<<<<<<< HEAD

    def number_of_rugbymen(self):
        return len(self._rugbymen)

    # plural
    def show_rugbymen(self):
        return self._rugbymen
=======
    
>>>>>>> branche_de_felix2


    def show_rugbyman(self, i):
        return self._chosen_rugbymen[i]
    
    def add_rugbyman(self, rugbyman):
        self._chosen_rugbymen.append(rugbyman)
    
    def refresh_deck(self):
        self._deck=cards.full_deck()

<<<<<<< HEAD
    def available_actions(self, rugbyman, game):
        available = []
        if (
            available_move_positions(
                rugbyman.posx(), rugbyman.posy(), rugbyman.moves_left(), game
            )
            != []
        ):
            available.append(actions.Action.MOVE)
            print("To move a player, write " + Action.MOVE)
        if (
            available_pass_positions(
                self.color(),
                rugbyman.posx(),
                rugbyman.posy(),
                rugbyman.pass_scope(),
                game,
            )
            != []
        ):  # définir rugbyman.pass_scope()
            available.append(actions.Action.PASS)
            print("To pass the ball to a player, write " + Action.PASS)
        if (
            available_tackle_positions(
                self.color(),
                rugbyman.posx(),
                rugbyman.posy(),
                rugbyman.tackle_scope(),
                game,
            )
            != []
        ):  # définir rugbyman.tackle_scope()
            available.append(actions.Action.TACKLE)
            print("To tackle a player, write " + Action.TACKLE)
        if (
            available_forward_pass(
                self.color(),
                rugbyman.posx(),
                rugbyman.posy(),
                rugbyman.forward_pass_scope(),
                game,
            )
            != []
        ):  # définir rugbyman.forward_pass_scope()
            available.append(actions.Action.FORWARD_PASS)
            print("To realize a forward pass, write " + Action.FORWARD_PASS)
        if available_score(self.color(), rugbyman.posx(), game) != []:
            available.append(actions.Action.SCORE)
            print("To score a try, write " + actions.Action.SCORE)

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
=======
    def refresh_rugbymen_stats(self):
        
        if len(self.get_deck())==0 :
            self._deck=cards.full_deck()
        for rugbyman in self.get_rugbymen():
            rugbymen.Rugbyman.refresh_stats(rugbyman)
        self._chosen_rugbymen= []
        self.can_play = True
>>>>>>> branche_de_felix2


    def get_deck_int(self):
        R=[]
        for card in self._deck:
            R.append(cards.convert_card_to_int(card))
        return R
    
    def get_deck(self):
        return self._deck
    
    def choose_card(self,card):
        if card in self.get_deck():
            self._deck.remove(card)
            return True
        else:
            return False
    

