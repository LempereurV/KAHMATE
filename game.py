import rugbymen
import players
import random
import actions
<<<<<<< HEAD
from color import Color

number_rugbymen = 6
number_of_rows = 8
number_of_columns = 11
forward_pass_scope = 3


class Game:
    def __init__(self):
        self.n_rugbymen = number_rugbymen
        self.n_columns = number_of_columns
        self.n_rows = number_of_rows
        # forward_pass_scope = forward_pass_scope
        self.red_player = players.Player(Color.RED)
        self.blue_player = players.Player(Color.BLUE)
        ball = players.Ball(random.randint(1, number_of_rows - 2))
=======
import color
import ball
import front 
from constants import *




class Game:
    """
    The Game class is the most "macroscopic" class of the code, it provides a general link between every class 
    """
    def __init__(self,Graphique):
        """
        The Game class contain s 
        """
>>>>>>> branche_de_felix2

        self._whose_turn = color.Color.RED

<<<<<<< HEAD
    def max_x(self):
        return self.n_columns - 1

    def max_y(self):
        return self.n_rows - 1
=======
        #player ne s'initialise pas pour rouge et bleu
        self._player_red = players.Player(color.Color.RED,self,self._whose_turn,Graphique) 
        self._player_blue = players.Player(color.Color.BLUE,self,self._whose_turn,Graphique) 

>>>>>>> branche_de_felix2

        #A changer
        self._ball = ball.Ball(random.randint(1, Constants.number_of_rows ))

<<<<<<< HEAD
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
=======

    
    def is_position_correct(self, x, y):
        return x >=1 and x <= Constants.number_of_rows and y >= 0 and y <= Constants.number_of_columns+1


    
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
    
>>>>>>> branche_de_felix2

    

    def which_rugbyman_in_pos(self,pos):
        for rugbyman in self.rugbymen():
            if (rugbymen.Rugbyman.get_pos(rugbyman) == pos and rugbyman.get_KO()==0):
                return rugbyman
        return False
    
    def what_is_in_pos(self,Graph):
        """
        The role of what_is_in_pos is wait for the user to click on the board and return the object that the user has clicked on
        These objects are either :
        -A rugbyman --> returns a rugbyman  
        -The ball --> returns the ball
        -Nothing --> returns False 
        -Skip button --> returns True 
        """
        pos,cond = Graph.get_hitbox_on_click()

        L_RED_skip_button=[[Constants.number_of_rows+1,i] for i in range(5)]
        L_BLUE_skip_button=[[0,Constants.number_of_columns+1-i] for i in range(5)]

        if (pos in L_RED_skip_button
            and self.get_player_turn().get_color()==color.Color.RED):
            Graph.highlight_button_after_click(color.Color.RED)
            return True
        if (pos in L_BLUE_skip_button
            and self.get_player_turn().get_color()==color.Color.BLUE):
            Graph.highlight_button_after_click(color.Color.BLUE)
            return True

        if (self.which_rugbyman_in_pos(pos) in self.get_player_turn().get_rugbymen()
            and cond
            and self.which_rugbyman_in_pos(pos).get_possesion()
            ):
            return self.get_ball()
        else :
            for rugbyman in self.rugbymen():
                if rugbymen.Rugbyman.get_pos(rugbyman) == pos :
                    if not bool(rugbyman.get_KO()) and rugbyman.get_moves_left() > 0:
                        return rugbyman
                    else:
                        return False
            return False

    def is_square_empty(self, x,y):
        for rugbyman in self.rugbymen():
            if rugbyman.get_pos_x() == x and rugbyman.get_pos_y() == y:
                return False
        return True
    #  available_move_position_recursif returns the list of all the possible positions (including the initial position) that a rugbyman can move to
    # Be aware that the elements of the list arent unique, the unicity will be given by available_move_position
    def available_move_position_recursif(self, rugbyman, x , y , scope, color, cond):
        """
        This function spread over on the board on all the reachable square (reachable squares are squares that are within the board limits 
        and do not contain ally rugbyman )
        The return shape is as follow :
        [x position of the square, y position of the square, movement points left to get to this square, Bool (True if square is free/ False if it contains an ennemy) ]
        """
        if scope < 0:
            return []
        else:
            R=[[x,y,scope,cond]]
            if x + 1 <= Constants.number_of_rows :
                if self.is_square_empty(x + 1, y):
                    R = R + self.available_move_position_recursif(rugbyman,x + 1, y, scope - 1,color,True)
                elif (self.which_rugbyman_in_pos([x + 1, y])!=False 
                      and self.which_rugbyman_in_pos([x + 1, y]).get_color()!=color):
                    if scope>0:
                        R = R + R + [[x+1,y,scope-1,False]]
            if x - 1 >= 1 :
                if self.is_square_empty(x - 1, y):
                    R = R + self.available_move_position_recursif(rugbyman,x - 1, y, scope - 1,color,True)
                elif ( self.which_rugbyman_in_pos([x - 1, y])!=False
                      and self.which_rugbyman_in_pos([x - 1, y]).get_color()!=color):
                    if scope>0:
                        R = R + [[x-1,y,scope-1,False]]
            if y + 1 <= Constants.number_of_columns+1 :
                if self.is_square_empty(x, y + 1):
                    R = R + self.available_move_position_recursif(rugbyman,x, y + 1, scope - 1,color,True)
                elif ( self.which_rugbyman_in_pos([x , y+1])!=False 
                      and self.which_rugbyman_in_pos([x, y + 1]).get_color()!=color):
                    if scope>0:
                        R = R + R + [[x,y+1,scope-1,False]]
            if y - 1 >= 0 :
                if self.is_square_empty(x, y - 1):
                    R = R + self.available_move_position_recursif(rugbyman,x, y - 1, scope - 1,color,True)
                elif ( self.which_rugbyman_in_pos([x , y-1])!=False and 
                      self.which_rugbyman_in_pos([x, y - 1]).get_color()!=color):
                    if scope>0:
                        R = R + R + [[x,y-1,scope-1,False]]

            #La condition suivante est à enlever si on veut que le rugbyman ne puisse sortir du terrain qu'avec la balle
            #Dans ce cas on ne peut pas gagner en passant dans la zone d'en-but adverse
            """
            #Case where the rughbyman is reaching outside of the board
            if (y +1 == self.get_number_of_columns()
                and scope>0
                and rugbyman.has_ball()):
                R = R + R + [[x,y+1,scope-1,True]]
            
            
            if (y-1==-1
                and scope>0
                and rugbyman.has_ball()):
                R = R + R + [[x,y-1,scope-1,True]]
            """
            
            return R
    def is_game_over(self):
        """
        The function is_game_over is over check one of the rugbymen is in the opposing goal with the ball:  
        If there is one --> returns True
        If not --> returns False
        """
        for rugbyman in self.rugbymen():
            if (rugbyman.get_pos_y()==0
                and rugbyman.get_color()==color.Color.BLUE
                and rugbyman.get_possesion()):
                print("Game over, the blue team won")
                return True
            if (rugbyman.get_pos_y()==Constants.number_of_columns+1 
                and rugbyman.get_color()==color.Color.RED
                and rugbyman.get_possesion()):
                print("Game over, the red team won")
                return True
        return False





    def available_move_position(self,rugbyman):

        """
        The main role of this function if to filter the data returned by the available_move_position_recursif function.
        This step is necessary since the data returned by available_move_position_recursif are not unique and are associated with
        different cost of mouvement  

        """
        
        Liste_untreated=self.available_move_position_recursif(rugbyman,rugbyman.get_pos_x(),rugbyman.get_pos_y(),rugbyman.get_moves_left(),rugbyman.get_color(),True)
        
        #Liste_untreated is a list of list of the form [x,y,scope,cond]
        #The goal here is to select the minimum distance for each position reachable
        Liste_untreated = sorted(Liste_untreated, key=lambda x: (x[0], x[1],x[2]), reverse=True)
        
        #Deleting the duplicates
        Liste_treated=[]
        i=0
        while i<len(Liste_untreated):
            if Liste_untreated[i][2]!=rugbyman.get_moves_left():
                Liste_treated.append(Liste_untreated[i])
            j=i
            while (j<len(Liste_untreated) 
                   and Liste_untreated[j][0]==Liste_untreated[i][0]
                   and Liste_untreated[j][1]==Liste_untreated[i][1]):
                j+=1
            i=j
        return Liste_treated
    

        
    #def unavailable_moove_position(self,rugbyman):

    

    
    def refresh_players_rugbymen_stats(self):
        """
        This function refresh the stats of every rugbyman of the game
        """
        players.Player.refresh_rugbymen_stats(self._player_red)
        players.Player.refresh_rugbymen_stats(self._player_blue)






    def get_ball(self):
        return self._ball

    def is_rugbyman_on_ball(self):
        """
        Check if there is a rugbyman on ball returns the rugbyman if there is return False otherwise
        """
        for rugbyman in self.rugbymen():
            if rugbyman.get_pos() == self.get_ball().get_pos():
                rugbyman.set_possesion(True)
                return rugbyman
        return False