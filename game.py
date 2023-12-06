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

        self._whose_turn = color.Color.RED

        #player ne s'initialise pas pour rouge et bleu
        self._player_red = players.Player(color.Color.RED,self,self._whose_turn,Graphique) 
        self._player_blue = players.Player(color.Color.BLUE,self,self._whose_turn,Graphique) 



        ball = players.Ball(random.randint(0, number_of_rows - 1))




    def get_number_of_rows(self):
        return self._number_of_rows
    
    def get_number_of_columns(self):
        return self._number_of_columns
    
    def get_player_red(self):
        return self._player_red
    
    def get_player_blue(self):
        return self._player_blue
    
    def get_player_turn(self):
        if self._whose_turn == color.Color.RED:
            return self.get_player_red()
        else:
            return self.get_player_blue()

    
    def change_player_turn(self):
        if self._whose_turn == color.Color.RED:
            self._whose_turn = color.Color.BLUE
        else:
            self._whose_turn = color.Color.RED

    def rugbymen(self):
        return players.Player.get_rugbymen( self.get_player_red()) + players.Player.get_rugbymen(self.get_player_blue())
    

    def which_rugbyman_in_pos(self,Graph):
        pos = Graph.get_hitbox_for_back()
        x=pos[0]
        y=pos[1]
        for rugbyman in self.rugbymen():
            if rugbymen.Rugbyman.get_posx(rugbyman) == x and rugbymen.Rugbyman.get_posy(rugbyman) == y:
                return rugbyman
        return False
    

    def is_square_empty(self, x, y):
        for rugbyman in self.rugbymen():
            if rugbyman.get_posx() == x and rugbyman.get_posy() == y:
                return False
        return True
    #  available_move_position_recursif returns the list of all the possible positions (including the initial position) that a rugbyman can move to
    # Be aware that the elements of the list arent unique, the unicity will be given by available_move_position
    def available_move_position_recursif(self, x , y , scope):
        if scope < 0:
            return []
        else:
            R=[[x,y]]
            if x + 1 < self.get_number_of_rows() and self.is_square_empty(x + 1, y):
                R = R + self.available_move_position_recursif(x + 1, y, scope - 1)

            if x - 1 >= 0 and self.is_square_empty(x - 1, y):
                R = R + self.available_move_position_recursif(x - 1, y, scope - 1)
            
            if y + 1 < self.get_number_of_columns() and self.is_square_empty(x, y + 1):
                R = R + self.available_move_position_recursif(x, y + 1, scope - 1)
            
            if y - 1 >= 0 and self.is_square_empty(x, y - 1):
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



    def forward_pass_scope(self):
        return self.forward_pass_scope


    def get_ball(self):
        return self.ball
