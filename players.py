import rugbymen
import cards
import tools


class Player:
    def __init__(self, color, game, turn_color, graphics, AI=False):

        # Placement order of the rugbylen (mostly for the initialisation but can be usefull later)
        self._placement_order = tools.placement_orders(color)

        # List of all the rugbymen of the player

        if AI:
            self._rugbymen = tools.positions_rugbymen_player_blue_AI(
                self._placement_order, graphics
            )
        else:
            self._rugbymen = tools.positions_rugbymen_player(
                self._placement_order, graphics
            )

        # List of all the rugbymen chosen by the player for his turn
        self._chosen_rugbymen = []

        self._deck = cards.full_deck()

        self._color = color
        if color == turn_color:
            self.can_play = True
        else:
            self.can_play = False

    def has_ball(self):
        """
        Return True if the player has the ball, False otherwise
        """
        for rugbyman in self.get_rugbymen():
            if rugbyman.has_ball():
                return True
        return False

    def get_color(self):
        return self._color

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

    def reset_player_after_turn(self):
        self._chosen_rugbymen = []
        self.can_play = True

    def get_can_play(self):
        return self.can_play

    def set_can_play(self, boolean):
        self.can_play = boolean

    def actualize_can_play(self):
        cond = False
        if self.get_deck() == []:
            self.refresh_deck()
        if self.get_n_rugbymen() >= 2:
            move_points = 0
            for rugbyman in self.get_chosen_rugbymen():
                if rugbyman.get_KO() == 0 and (
                    rugbymen.Rugbyman.move_left(rugbyman) > 0 or rugbyman.has_ball()
                ):
                    cond = True
                move_points += rugbymen.Rugbyman.move_left(rugbyman)
            if not cond:
                self.set_can_play(False)
            else:
                if move_points == 0:
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

    def show_rugbyman(self, i):
        return self._chosen_rugbymen[i]

    def add_rugbyman(self, rugbyman):
        self._chosen_rugbymen.append(rugbyman)

    def refresh_deck(self):
        self._deck = cards.full_deck()

    def refresh_rugbymen_stats(self):

        if len(self.get_deck()) == 0:
            self._deck = cards.full_deck()
        for rugbyman in self.get_rugbymen():
            rugbymen.Rugbyman.refresh_stats(rugbyman)
        self._chosen_rugbymen = []
        self.can_play = True

    def get_deck_int(self):
        R = []
        for card in self._deck:
            R.append(cards.convert_card_to_int(card))
        return R

    def get_deck(self):
        return self._deck

    def choose_card(self, card):
        if card in self.get_deck():
            self._deck.remove(card)
            if len(self.get_deck()) == 0:
                self.refresh_deck()
            return True
        else:
            return False

    ###Fonctions nécessaires pour l'IA ###

    def get_moves_left(self):
        if len(self.get_chosen_rugbymen()) < 2:
            return 1
        else:
            for rugbyman in self.get_chosen_rugbymen():
                if rugbyman.get_moves_left() > 0:
                    return 1
            return 0

    def undo_chosen_rugbymen(self):
        new_chosen_rugbymen = []
        for rugbyman in self.get_chosen_rugbymen():
            if not rugbyman.get_moves_left() == rugbyman.get_move_points():
                new_chosen_rugbymen.append(rugbyman)
        self._chosen_rugbymen = new_chosen_rugbymen
