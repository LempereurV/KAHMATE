import rugbymen
import players
import random
import actions


number_of_rows = 8
number_of_columns = 11
forward_pass_scope = 3


class Game:
    def __init__(self):
        self.max_x_value = number_of_columns - 1
        self.max_y_value = number_of_rows - 1
        # ...
        #forward_pass_scope = forward_pass_scope
        #player1 = players.Player("blue") #à modifier ici et dans actions.pass_ball() et rugbymen.rugbyman
        #player2 = players.Player("red") #idem
        ball = players.Ball(random.randint(0,number_of_rows - 1))

    def is_over(self):
        pass

    def max_x(self):
        return self.max_x_value
    
    def max_y(self):
        return self.max_y_value

    def forward_pass_scope(self):
        return self.forward_pass_scope

    def blue_player(self):
        return self.player1

    def red_player(self):
        return self.player2

    def rugbymen(self):
        return self.player1.rugbymen() + self.player2.rugbymen()

    def is_position_valid(self, position):
        return ((position[0] >= 0) 
                and (position[0] <= self.max_x()) 
                and (position[1] >= 0) 
                and (position[1] <= self.max_y()))

    def is_position_unoccupied(self, position):
        for rugbyman in self.players():
            if [rugbyman.posx(), rugbyman.posy()] == position:  # Fixed: Use '==' for comparison
                return False
        return True
    
    def is_position_occupied_by_team(self, color, position, game):
        for rugbyman in game.rugbymen():
            if (color is rugbyman.color()
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
