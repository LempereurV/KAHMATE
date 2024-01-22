import players
import random
import actions
import color
import ball
from constants import *
import actions
import time 

class Game:
    """
    The Game class is the most "macroscopic" class of the code, it provides a general link between every class 
    """
    def __init__(self,graphique):
        """
        The Game class is the most "macroscopic" class of the code, it provides a general link between every class
        """

        self._whose_turn = color.Color.RED

        #player ne s'initialise pas pour rouge et bleu
        self._player_red = players.Player(color.Color.RED,self,self._whose_turn,Graphique) 
        self._player_blue = players.Player(color.Color.BLUE,self,self._whose_turn,Graphique) 


        #A changer
        self._ball = ball.Ball(random.randint(1, Constants.number_of_rows ))


    
    def is_position_correct(self, x, y):
        """
        Returns a boolean that indicates if the pos is within the board limits
        """
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
    

    

    def which_rugbyman_in_pos(self,pos):
        for rugbyman in self.rugbymen():
            if (rugbyman.get_pos() == pos and rugbyman.get_KO()==0):
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
                if rugbyman.get_pos() == pos :
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
    
    def available_move_position_recursif(self, rugbyman, x,y , scope, color, cond,moves_dictionnary):
        """
        This function spread over on the board on all the reachable square (reachable squares are squares that are within the board limits 
        and do not contain ally rugbyman )
        The return shape is as follow :
        [x position of the square, y position of the square, movement points left to get to this square, Bool (True if square is free/ False if it contains an ennemy) ]
        """
        pos=[x,y]
        if scope >= 0:
            
            if tuple(pos) in moves_dictionnary:
                moves_dictionnary[tuple(pos)]=[max(moves_dictionnary[tuple(pos)][0],scope),cond]
            else:
                moves_dictionnary[tuple(pos)]=[scope,cond]

            if x + 1 <= Constants.number_of_rows :
                if self.is_square_empty(x + 1, y):
                    self.available_move_position_recursif(rugbyman,x + 1, y, scope - 1,color,True,moves_dictionnary)
                elif (self.which_rugbyman_in_pos([x + 1, y])!=False 
                        and self.which_rugbyman_in_pos([x + 1, y]).get_color()!=color
                        and (self.which_rugbyman_in_pos([x + 1, y]).has_ball()
                        or rugbyman.has_ball())):
                    if scope>0:
                        if tuple([x+1,y]) in moves_dictionnary:
                            moves_dictionnary[tuple([x+1,y])]=[max(moves_dictionnary[tuple([x+1,y])][0],scope-1),False]
                        else :
                            moves_dictionnary[tuple([x+1,y])]=[scope-1,False]
            if x - 1 >= 1 :
                if self.is_square_empty(x - 1, y):
                    self.available_move_position_recursif(rugbyman,x - 1, y, scope - 1,color,True,moves_dictionnary)
                elif ( self.which_rugbyman_in_pos([x - 1, y])!=False
                        and self.which_rugbyman_in_pos([x - 1, y]).get_color()!=color
                        and (self.which_rugbyman_in_pos([x - 1, y]).has_ball()
                             or rugbyman.has_ball())):
                    if scope>0:
                        if tuple([x-1,y]) in moves_dictionnary:
                            moves_dictionnary[tuple([x-1,y])]=[max(moves_dictionnary[tuple([x-1,y])][0],scope-1),False]
                        else:
                            moves_dictionnary[tuple([x-1,y])]=[scope-1,False]
                            
            if y + 1 <= Constants.number_of_columns+1 :
                if self.is_square_empty(x, y + 1):
                    self.available_move_position_recursif(rugbyman,x, y + 1, scope - 1,color,True,moves_dictionnary)
                elif ( self.which_rugbyman_in_pos([x , y+1])!=False 
                        and self.which_rugbyman_in_pos([x, y + 1]).get_color()!=color
                        and (self.which_rugbyman_in_pos([x, y + 1]).has_ball()
                             or rugbyman.has_ball())):
                    if scope>0:
                        if tuple([x,y+1]) in moves_dictionnary:
                            moves_dictionnary[tuple([x,y+1])]=[max(moves_dictionnary[tuple([x,y+1])][0],scope-1),False]
                        else :
                            moves_dictionnary[tuple([x,y+1])]=[scope-1,False]
            if y - 1 >= 0 :
                if self.is_square_empty(x, y - 1):
                    self.available_move_position_recursif(rugbyman,x, y - 1, scope - 1,color,True,moves_dictionnary)
                elif ( self.which_rugbyman_in_pos([x , y-1])!=False and 
                        self.which_rugbyman_in_pos([x, y - 1]).get_color()!=color
                        and (self.which_rugbyman_in_pos([x, y - 1]).has_ball()
                             or rugbyman.has_ball())):
                    if scope>0:
                        if tuple([x,y-1]) in moves_dictionnary:
                            moves_dictionnary[tuple([x,y-1])]=[max(moves_dictionnary[tuple([x,y-1])][0],scope-1),False]
                        else :
                            moves_dictionnary[tuple([x,y-1])]=[scope-1,False]
    
    def available_move_position(self,rugbyman):
        
        moves_dictionnary={}
        self.available_move_position_recursif(rugbyman,rugbyman.get_pos_x(),rugbyman.get_pos_y(),rugbyman.get_moves_left(),rugbyman.get_color(),True,moves_dictionnary)
        Liste_treated=[[key[0],key[1], value[0],value[1]] for key, value in moves_dictionnary.items() if (key[0]!=rugbyman,rugbyman.get_pos_x() and key[1]!=rugbyman.get_pos_y())] 

        
        return Liste_treated
      
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
        Check if there is a rugbyman on ball returns the rugbyman if True ; return False otherwise
        """
        for rugbyman in self.rugbymen():
            if rugbyman.get_pos() == self.get_ball().get_pos():
                rugbyman.set_possesion(True)
                return rugbyman
        return False
    
    ### Fonctions nécessaires pour l'IA ###

    def reward_function(self,player):
        """
        This function is used to evaluate the state of the game
        """
        reward=random.random()
        #The award is a number, the higher the better for the red player and the lower the better for the blue player

        #The distance between the ball and the middle field can be viewed as the distance between the ball and the goal
        #It is good for the ball to be close to the opponent goal and bad for the ball to be close to his own goal
        reward+=player.has_ball()*100
        
        reward += (self.get_ball().get_pos_y()-(Constants.number_of_columns+1)//2)*20
        
        if player.get_color()==color.Color.RED:
            for rugbyman in player.get_rugbymen():
                if rugbyman.get_possesion():
                        reward+=10
                #It is better for the rugbymen to be generally close to the ball 
                reward+=-actions.norm(rugbyman.get_pos(),self.get_ball().get_pos())*10

        if player.get_color()==color.Color.BLUE:
            for rugbyman in player.get_rugbymen():
                if rugbyman.get_possesion():
                        reward-=10
                #It is better for the rugbymen to be generally close to the ball 
                reward+=actions.norm(rugbyman.get_pos(),self.get_ball().get_pos())*10
        
        return reward

    def every_possible_move(self,player):
        """
        This function returns a list of all the possible moves of a player sorted by proximity with the ball 
        """
        R=[]

        for rugbyman in player.get_rugbymen():
            if rugbyman.get_move_points()==rugbyman.get_moves_left():
                R=[[rugbyman]+self.available_move_position(rugbyman)]+R
        return sorted(R,key =lambda x:actions.norm(x[0].get_pos(),self.get_ball().get_pos()))

    def other_player(self,player):
        """
        This function returns the other player
        """
        if player==self._player_red:
            return self._player_blue
        return self._player_red

def every_possible_move_naif(self,player):
    """
    This function returns a list of all the cases directly adjacent to the player
    """
    R=[]
    for rugbyman in player.get_rugbymen():
        if rugbyman.get_move_points()==rugbyman.get_moves_left():
            if rugbyman.get_pos_x()+1<=Constants.number_of_rows and self.is_square_empty(rugbyman.get_pos_x()+1,rugbyman.get_pos_y()):
                R.append([rugbyman.get_pos_x()+1,rugbyman.get_pos_y(),rugbyman.get_move_points()-1,True])
            if rugbyman.get_pos_x()-1>=1 and self.is_square_empty(rugbyman.get_pos_x()-1,rugbyman.get_pos_y()):
                R.append([rugbyman.get_pos_x()-1,rugbyman.get_pos_y(),rugbyman.get_move_points()-1,True])
            if rugbyman.get_pos_y()+1<=Constants.number_of_columns+1 and self.is_square_empty(rugbyman.get_pos_x(),rugbyman.get_pos_y()+1):
                R.append([rugbyman.get_pos_x(),rugbyman.get_pos_y()+1,rugbyman.get_move_points()-1,True])
            if rugbyman.get_pos_y()-1>=0 and self.is_square_empty(rugbyman.get_pos_x(),rugbyman.get_pos_y()-1):
                R.append([rugbyman.get_pos_x(),rugbyman.get_pos_y()-1,rugbyman.get_move_points()-1,True])
    return [rugbyman]+R
            