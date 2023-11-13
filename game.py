import rugbymen
import players
import random
import actions


number_of_rows = 8
number_of_columns = 11
forward_pass_scope = 3

class Game:
    def __init__(self):
        max_x = number_of_columns - 1
        max_y = number_of_rows - 1
        forward_pass_scope = forward_pass_scope
        player1 = players.Player("blue") #à modifier ici et dans actions.pass_ball() et rugbymen.rugbyman
        player2 = players.Player("red") #idem
        ball = players.Ball(random.randint(0,number_of_rows - 1))

    def is_over(self):
        pass

    def max_x(self):
        return self.max_x
    
    def max_y(self):
        return self.max_y

    def forward_pass_scope(self):
        return self.forward_pass_scope
    
    def blue_player(self):
        return self.player1
    
    def red_player(self):
        return self.player2

    def players(self):
        return self.player1.players() + self.player2.players()

    def is_position_valid(self, position):
        return ((position[0] >= 0) 
                and (position[0] <= self.max_x) 
                and (position[1] >= 0) 
                and (position[1] <= self.max_y))

    def is_position_unoccupied(self, position):
        for rugbyman in self.players():
            if [rugbyman.posx(), rugbyman.posy()] is position:
                return False
        return True

    def play(self):
        while not self.is_over:
            pass
    
    def ball(self):
        return self.ball