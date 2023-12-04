import numpy as np
import rugbymen
import front
from color import Color
import random
import actions

n_row = 8
n_column = 11
n_case = n_row * n_column
n_rugbymen = 6


class Board:
    def __init__(self, Graphique):
        red_position = actions.positions_rugbymen_player(
            Color.RED, n_rugbymen, n_column, Graphique
        )
        blue_position = actions.positions_rugbymen_player(
            Color.BLUE, n_rugbymen, n_column, Graphique
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
        scope = rubgyman.moves_left()
        return self.available_move_position_recursif(pos, scope, cond_first_layer)

    def move_rugbyman(self, pos, possible_move, Graphique):
        pos2 = front.Graphique.get_hitbox_for_back(Graphique)
        if pos2 in possible_move:
            self._board[pos2[0]][pos2[1]] = self._board[pos[0]][pos[1]]
            self._board[pos[0]][pos[1]] = None
            self._board[pos2[0]][pos2[1]].actualize_move_left(
                abs(pos2[0] - pos[0]) + abs(pos2[1] - pos[1])
            )
            return True
        else:
            print("The move isn't allowed")
            return False

    def refresh_rugbymen_stats(self):
        for i in range(n_row):
            for j in range(n_column):
                if self._board[i][j] != None:
                    self._board[i][j].refresh_stats()
