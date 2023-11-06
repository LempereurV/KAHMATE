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


def placement_order(color):
    R = {
        "First Normal Rugbyman": rugbymen.Rugbyman(color),
        "Second Normal Rugbyman": rugbymen.Rugbyman(color),
        "Strong Rugbyman": rugbymen.Strong_rugbyman(color),
        "Hard Rugbyman": rugbymen.Hard_rugbyman(color),
        "Smart Rugbyman": rugbymen.Smart_rugbyman(color),
        "Fast Rugbyman": rugbymen.Fast_rugbyman(color),
    }
    return R


def positions_rugbymen_player(color, placement_order):
    i = 0
    R = np.zeros((n_rugbymen, 2))
    # The  player chooses his rugbymen positions
    while i < n_rugbymen:
        print("Choose the position of the " + placement_order.keys(i))
        pos = front.get_hitbox()[1]
        if color == Color.RED:
            while pos[0] > 4:
                print(
                    "The position isn't correct, the red team is suppose to be on the left "
                )
                pos = front.display_number(front.hitbox)
        if color == Color.BLUE:
            while pos[0] < 6:
                print(
                    "The position isn't correct, the blue team is suppose to be on the right "
                )
                pos = front.display_number(front.hitbox)
        self.coords[pos[0]][pos[1]] = placement_order[placement_order.keys(i)]
        i += 1


class board:
    def __init__(self, blue_position, red_position):
        self._board = np.zeros((n_row, n_column))
        assert len(red_position) == n_rugbymen
        assert len(blue_position) == n_rugbymen

        for p in blue_position:
            self._board[p[0]][p[1]] = 1
        for p in red_position:
            self._board[p[0]][p[1]] = 2

        self.coords = np.zeros(())  # Not yet defined outside
        i = 0
        # The red player chooses his rugbymen positions
        while i < n_rugbymen:
            print("Choose the position of the " + placement_order.keys(i))
            pos = front.display_number(front.hitbox)
            while pos[0] > 4:
                pos = front.display_number(front.hitbox)
                print(
                    "The position isn't correct, the red team is suppose to be on the left "
                )
            self.coords[pos[0]][pos[1]] = placement_order[placement_order.keys(i)]
            i += 1

        # The blue player chooses his rugbymen positions
        i = 0
        pos = front.display_number(front.hitbox)
        while i < n_rugbymen:
            print("Choose the position of the " + placement_order.keys(i))
            pos = front.display_number(front.hitbox)
            while pos[0] < 6:
                pos = front.display_number(front.hitbox)
                print(
                    "The position isn't correct, the red team is suppose to be on the left "
                )
            self.coords[pos[0]][pos[1]] = placement_order[placement_order.keys(i)]
            i += 1
