import rugbymen
import players
import random
import actions
from color import Color

number_of_rows = 8
number_of_columns = 11
forward_pass_scope = 3


class Game:
    def __init__(self):
        self.n_columns = number_of_columns
        self.n_rows = number_of_rows
        #forward_pass_scope = forward_pass_scope
        self.red_player = players.Player(Color.RED)
        self.blue_player = players.Player(Color.BLUE)
        ball = players.Ball(random.randint(1,number_of_rows - 2))

    def is_over(self):
        pass

    def max_x(self):
        return self.n_columns - 1
    
    def max_y(self):
        return self.n_rows - 1

    def forward_pass_scope(self):
        return self.forward_pass_scope

    def player(self, color):
        if color is Color.RED:
            return self.red_player
        if color is Color.BLUE:
            return self.blue_player
        
    def player_play(self, color):
        player = self.player(color)
        return player.play()

    def all_rugbymen(self):
        return self.player1.rugbymen() + self.player2.rugbymen()

    def is_position_valid(self, position):
        return (
            (position[0] >= 0)
            and (position[0] <= self.max_x())
            and (position[1] >= 0)
            and (position[1] <= self.max_y())
        )

    def is_position_unoccupied(self, position):
        for rugbyman in self.players():
            if [
                rugbyman.posx(),
                rugbyman.posy(),
            ] == position:  # Fixed: Use '==' for comparison
                return False
        return True

    def is_position_occupied_by_team(self, color, position, game):
        for rugbyman in game.rugbymen():
            if (
                color is rugbyman.color()
                and position[0] == rugbyman.posx()
                and position[1] == rugbyman.posy()
            ):
                return True
        return False

    def play(self):
        while not self.is_over:
            pass

    def ball(self):
        return self.ball
