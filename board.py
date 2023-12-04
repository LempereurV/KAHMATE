import numpy as np
import rugbymen
import front
from color import Color
import random

n_row = 8
n_column = 11
n_case = n_row * n_column
n_rugbymen = 6


def placement_orders(color):
    R = {
        "First Normal Rugbyman": rugbymen.Rugbyman(color),
        "Second Normal Rugbyman": rugbymen.Rugbyman(color),
        "Strong Rugbyman": rugbymen.StrongRugbyman(color),
        "Hard Rugbyman": rugbymen.HardRugbyman(color),
        "Smart Rugbyman": rugbymen.SmartRugbyman(color),
        "Fast Rugbyman": rugbymen.FastRugbyman(color),
    }
    return R


def positions_rugbymen_player(color, Graphique):
    placement_order = placement_orders(color)

    i = 0
    R = [None] * n_rugbymen  # R is the list of the positions of the rugbymen
    Noms = list(placement_order.keys())  # List of the names of the rugbymen

    ### A enlever ####
    for i in range(n_rugbymen):
        if color == Color.RED:
            R[i] = [i, random.randint(0, 4), placement_order[Noms[i]]]
        else:
            R[i] = [i, random.randint(6, 10), placement_order[Noms[i]]]
        front.Graphique.affiche_joueur(
            Graphique,
            11 * R[i][0] + R[i][1],
            front.path_convertor(placement_order[Noms[i]]),
        )
    return R
    ####    FIn a enlever

    while i < n_rugbymen:
        print(
            str(color).split(".")[-1] + " Player, Choose the position of the " + Noms[i]
        )  # Changer Color.split(".")[-1] for the color to display as intended
        pos = front.Graphique.get_hitbox_for_back(
            Graphique
        )  # Fonction de la classe graphique qui renvoie une liste de la forme [i,j] avec i et j les colonnes et lignes de la case cliquée
        if pos in R:
            cond_pos_already_taken = True
            while cond_pos_already_taken:
                print("The position chosen is already taken, re choose the position")
                pos = front.Graphique.get_hitbox_for_back(Graphique)
                if not pos in R:
                    cond_pos_already_taken = False
        if (
            color == Color.RED and pos[1] >= n_column // 2
        ):  # Red characters should be placed on the left
            cond_RED = True
            while cond_RED:
                print(
                    "The position isn't correct, the red team is suppose to be on the left, re choose the position"
                )
                pos = front.Graphique.get_hitbox_for_back(Graphique)
                if pos[1] < n_column // 2:
                    cond_RED = False

        if color == Color.BLUE and pos[1] <= n_column // 2:
            cond_Blue = True
            while cond_Blue:
                print(
                    "The position isn't correct, the blue team is suppose to be on the right, re choose the position"
                )
                pos = front.Graphique.get_hitbox_for_back(Graphique)
                if pos[1] > n_column // 2:
                    cond_Blue = False
        front.Graphique.affiche_joueur(
            Graphique,
            pos[0] * n_column + pos[1],
            front.path_convertor(placement_order[Noms[i]]),
        )  # Display the newly placed rugbymen on the board
        R[i] = [pos[0], pos[1]]
        i += 1
    R_with_rugbymen = []
    # R_with_rugbymen is the list of the positions of the rugbymen with the type of the rugbymen
    for i in range(n_rugbymen):
        R_with_rugbymen.append(R[i] + [placement_order[Noms[i]]])

    return R_with_rugbymen


class Board:
    def __init__(self, Graphique):
        red_position = positions_rugbymen_player(Color.RED, Graphique)
        blue_position = positions_rugbymen_player(
            Color.BLUE, Graphique
        )  # Attention, il faut le graphique board soit créé avant les joueurs
        self._board = [[None for j in range(n_column)] for i in range(n_row)]
        assert len(red_position) == n_rugbymen
        assert len(blue_position) == n_rugbymen
        for p in blue_position:
            self._board[p[0]][p[1]] = p[2]
        for p in red_position:
            self._board[p[0]][p[1]] = p[2]
        # xprint(self._board)

    def is_square_free(self, pos):
        # print(pos)
        return self._board[pos[0]][pos[1]] == None

    def which_rugbyman(self, pos):
        if self.is_square_free(pos) == False:
            return self._board[pos[0]][pos[1]]
        else:
            return False

    def available_move_position_recursif(self, pos, scope, cond_first_layer):
        if scope < 0:
            return []
        else:
            if cond_first_layer:
                R = []
                cond_first_layer = False
            else:
                R = [pos]
            if pos[0] + 1 < n_row and self.is_square_free([pos[0] + 1, pos[1]]):
                R = R + self.available_move_position_recursif(
                    [pos[0] + 1, pos[1]], scope - 1, cond_first_layer
                )
            if pos[0] - 1 >= 0 and self.is_square_free([pos[0] - 1, pos[1]]):
                R = R + self.available_move_position_recursif(
                    [pos[0] - 1, pos[1]], scope - 1, cond_first_layer
                )
            if pos[1] + 1 < n_column and self.is_square_free([pos[0], pos[1] + 1]):
                R = R + self.available_move_position_recursif(
                    [pos[0], pos[1] + 1], scope - 1, cond_first_layer
                )
            if pos[1] - 1 >= 0 and self.is_square_free([pos[0], pos[1] - 1]):
                R = R + self.available_move_position_recursif(
                    [pos[0], pos[1] - 1], scope - 1, cond_first_layer
                )
            unique_positions_set = set(map(tuple, R))
            unique_positions_list = [list(pos) for pos in unique_positions_set]
            return unique_positions_list

    def available_move_position(self, pos):
        cond_first_layer = True
        rubgyman = self.which_rugbyman(pos)
        scope = rubgyman.move_left()
        return self.available_move_position_recursif(pos, scope, cond_first_layer)

    def move_rugbyman(self, pos, possible_move, Graphique):
        pos2 = front.Graphique.get_hitbox_for_back(Graphique)
        if pos2 in possible_move:
            self._board[pos2[0]][pos2[1]] = self._board[pos[0]][pos[1]]
            self._board[pos[0]][pos[1]] = None
            self._board[pos2[0]][pos2[1]].actualize_move_left(
                abs(pos2[0] - pos[0]) + abs(pos2[1] - pos[1])
            )
            return pos2
        else:
            print("The move isn't allowed")
            return False

    def refresh_rugbymen_stats(self):
        for i in range(n_row):
            for j in range(n_column):
                if self._board[i][j] != None:
                    self._board[i][j].refresh_stats()
