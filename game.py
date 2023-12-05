import rugbymen
import players
import random
import actions
import color

number_of_rows = 8
number_of_columns = 11
forward_pass_scope = 3


class Game:
    def __init__(self,Graphique):
        self._number_of_columns = number_of_columns 
        self._number_of_rows = number_of_rows 

        #player ne s'initialise pas pour rouge et bleu
        self._player_red = players.Player(color.Color.RED,self,Graphique) 
        self._player_blue = players.Player(color.Color.BLUE,self,Graphique) 

        ball = players.Ball(random.randint(0, number_of_rows - 1))


    ### FELIX ###


    def get_number_of_rows(self):
        return self._number_of_rows
    
    def get_number_of_columns(self):
        return self._number_of_columns
    
    def get_player_red(self):
        return self._player_red
    
    def get_player_blue(self):
        return self._player_blue
    
    def rugbymen(self):
        return players.Player.get_rugbymen( self.get_player_red()) + players.Player.get_rugbymen(self.get_player_blue())
    

    def which_rugbyman_in_pos(self, x,y):

        for rugbyman in self.rugbymen():
            if rugbymen.Rugbyman.get_posx(rugbyman) == x and rugbymen.Rugbyman.get_posy(rugbyman) == y:
                return rugbyman
        return False
    

    #  available_move_position_recursif returns the list of all the possible positions (including the initial position) that a rugbyman can move to
    # Be aware that the elements of the list arent unique, the unicity will be given by available_move_position

    def available_move_position_recursif(self, x , y , scope):
        if scope < 0:
            return []
        else:
            R=[[x,y]]
            if x + 1 < self.get_number_of_rows() and self.which_rugbyman_in_pos(x + 1, y)==False:
                R = R + self.available_move_position_recursif(x + 1, y, scope - 1)

            if x - 1 >= 0 and self.which_rugbyman_in_pos(x - 1, y)==False:
                R = R + self.available_move_position_recursif(x - 1, y, scope - 1)
            
            if y + 1 < self.get_number_of_columns() and self.which_rugbyman_in_pos(x, y + 1)==False:
                R = R + self.available_move_position_recursif(x, y + 1, scope - 1)
            
            if y - 1 >= 0 and self.which_rugbyman_in_pos(x, y - 1)==False:
                R = R + self.available_move_position_recursif(x, y - 1, scope - 1)
            
            return R
    
    def available_move_position(self,rugbyman):
        
        Liste_untreated=self.available_move_position_recursif(rugbyman.get_posx(),rugbyman.get_posy(),rugbyman.get_moves_left())
        #Deleting the first position of the list because it is the position of the rugbyman
        Liste_untreated.remove([rugbyman.get_posx(),rugbyman.get_posy()])
        #Deleting the duplicates
        Liste_treated=[]
        for element in Liste_untreated:
            if element not in Liste_treated:
                Liste_treated.append(element)
        return Liste_treated
    

    
    def refresh_players_rugbymen_stats(self):
        players.Player.refresh_rugbymen_stats(self._player_red)
        players.Player.refresh_rugbymen_stats(self._player_blue)



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
