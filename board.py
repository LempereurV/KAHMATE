import numpy as np
import rugbymen
import front
import enum

n_row = 11
n_column = 8
n_case = n_row * n_column
n_rugbymen = 6



class Color(enum.Enum):
    RED = "red"
    BLUE = "blue"


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


def positions_rugbymen_player(color,graphique_board):
    placement_order = placement_orders(color)
    i = 0
    R = np.zeros((n_rugbymen, 2))
    # The  player chooses his rugbymen positions
    Noms=list(placement_order.keys())
    while i < n_rugbymen:
        print("Choose the position of the " + Noms[i])
        pos = graphique_board.get_hitbox()
        if pos is None:
            print("You must click on the board")
            return 0
        while (len(pos)<2):
            print("You must click on the board")

            pos = graphique_board.get_hitbox()
        
        if color == Color.RED:
            while pos[1][0] > 4:
                print(
                    "The position isn't correct, the red team is suppose to be on the left "
                )
                pos = graphique_board.get_hitbox()
        if color == Color.BLUE:
            while pos[1][0] < 6:
                print(
                    "The position isn't correct, the blue team is suppose to be on the right "
                )
                pos = graphique_board.get_hitbox()
        i += 1
        R[i] = pos[1]
    return R


class Board:
    def __init__(self, blue_position, red_position):
        self._board = np.zeros((n_row, n_column))
        assert len(red_position) == n_rugbymen
        assert len(blue_position) == n_rugbymen
        for p in blue_position:
            self._board[p[0]][p[1]] = 1
        for p in red_position:
            self._board[p[0]][p[1]] = 2

    def is_square_free(self, x, y):
        return self._board[x][y] == 0
    

placement_orders(Color.RED)