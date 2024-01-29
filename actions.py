import rugbymen
import front
import random
from color import Color
import players
import game
import ball
from constants import Constants
import cards   
import enum
import tools 

class ActionName(enum.Enum):
    MOVE = "move"
    PASS = "pass"
    TACKLE = "tackle"
    FORWARD_PASS = "forward_pass"
    SCORE = "score"




class Action:
    """
    This class allows an easier managment of rugbymen's actions on the board 

    """

    def __init__(self,game,graphique) :
        """
        Contains solely the Game instance and Graphique instance necessary to collect inputs 
        """
        self.game = game
        self.graphique = graphique


    def move_rugbyman(self,pos,rugbyman,cost):
        """
        Takes in arguments the pos to which the rugbyman should be moved, and the rugbyman itself

        This pos should always be empty and accessible no internal check besides assertions

        Does not return anything
        """
        
        ball=self.game.get_ball()

        if rugbyman.get_possesion():
            ball.set_pos(pos)
        
        rugbyman.set_pos(pos)
        rugbyman.set_move_left(cost)

        if rugbyman.get_pos()==ball.get_pos():
            ball.set_carrier(rugbyman)
            rugbyman.set_possesion(True)
        
        return rugbyman
        
        

    def move_rugbyman_after_succesfull_charging(self, rugbyman,possible_moves):
            """
            This function should only be used after a succesfull charge, once the attacking rugbyman is on the defender as 
            it forces the attacking rugbyman to change position 

            Takes into argument the attacking rugbyman and the list of possible moves for this rugbyman

            Does not return anything 
            """
            
            ball=self.game.get_ball()

            possible_moves_without_scope_and_bool = [[k[0],k[1]] for k in possible_moves]
            
            while True:
                pos,cond=self.graphique.get_hitbox_on_click()
                if pos in possible_moves_without_scope_and_bool:
                    i=possible_moves_without_scope_and_bool.index(pos)
                    if possible_moves[i][3]:
                        return self.move_rugbyman(pos,rugbyman,possible_moves[i][2])
                    else :
                        print("You can't move to this position")
                        
    def attacker_win_charge(self,rugbyman_attacker,rugbyman_defender,possible_moves):
        #Defender is KO
        rugbyman_defender.set_KO()

        #He loses the ball and attacker retreives it
        rugbyman_defender.set_possesion(False)
        self.game.get_ball().set_pos(rugbyman_defender.get_pos()) #A bit useless here since the ball was already in the defender position
        rugbyman_attacker.set_possesion(True)

        #Rugbyman attacker is on defender position we then actualize his position and move left
        rugbyman_attacker.set_pos(rugbyman_defender.get_pos())
        for move in possible_moves:
            if move[:2]==rugbyman_defender.get_pos():
                rugbyman_attacker.set_move_left(move[2])
        
        #We re-compute the list of possible moves for the attacker and make him move
        self.graphique.draw_board(self.game)
        possible_moves=self.game.available_move_position(rugbyman_attacker)
        self.graphique.highlight_move(possible_moves)
        #This function forces the rugbyman to move
        self.move_rugbyman_after_succesfull_charging(rugbyman_attacker,possible_moves)
                
    def defender_win_charge(self,rugbyman_attacker,rugbyman_defender,possible_moves):
        #If the defender wins the charge
        rugbyman_attacker.set_KO()
        
        #We then have to move the now lost ball to a new position 
        if rugbyman_attacker.get_color()==Color.RED:
            self.red_defender_win_charge(rugbyman_attacker,rugbyman_defender)
        else:
            self.blue_defender_win_charge(rugbyman_attacker,rugbyman_defender)
            
        rugbyman_attacker.set_possesion(False)
        
        #If the rugbyman doing the charging was far from the the defender we have to replace it like he made 
        #the move one square by one square
        if tools.norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>1:
            self.attacker_far_from_defender(rugbyman_attacker,rugbyman_defender,possible_moves)
        return rugbyman_attacker 

    def attacker_far_from_defender(self,rugbyman_attacker,rugbyman_defender,possible_moves):
        min_norm=100
        #we iterate over the possible moves of the attacker (moves where he could have been if he took the time to move 
        # his rugbyman one square by one square)
        for move in possible_moves:
            
            #The relocation has to be close to the defender
            if tools.norm(move[:2],rugbyman_defender.get_pos())==1:
                #The closest square is the natural choice
                if tools.norm(move[:2],rugbyman_attacker.get_pos())<min_norm:

                    min_norm=tools.norm([move[0],move[1]],rugbyman_attacker.get_pos())
                    new_attacker_pos=[move[0],move[1]]
                    new_attacker_cost=move[2]
        if min_norm<100:
            rugbyman_attacker.set_pos(new_attacker_pos)
            rugbyman_attacker.set_move_left(new_attacker_cost)
        if rugbyman_attacker.get_possesion():
            self.game.get_ball().set_pos(new_attacker_pos)


    def red_defender_win_charge(self,rugbyman_attacker,rugbyman_defender):
        if rugbyman_attacker.get_pos_y()>1:
                #The first normal position (happens 90% of the time) is just putting the ball behind the attacker
                self.game.get_ball().set_pos([rugbyman_attacker.get_pos_x(),rugbyman_attacker.get_pos_y()-1])
        else:
            
            #If the attacker is on the edge of the board we put the ball on the side
            if rugbyman_attacker.get_pos_x()>1:
                self.game.get_ball().set_pos([rugbyman_attacker.get_pos_x()-1,rugbyman_attacker.get_pos_y()])
            else:
                self.game.get_ball().set_pos([rugbyman_attacker.get_pos_x()+1,rugbyman_attacker.get_pos_y()])

    def blue_defender_win_charge(self,rugbyman_attacker,rugbyman_defender):
        #Same but here the "behind" blue is towards the right 
        if rugbyman_attacker.get_pos_y()<Constants.number_of_columns :
            self.game.get_ball().set_pos([rugbyman_attacker.get_pos_x(),rugbyman_attacker.get_pos_y()-1])
        else:
            if rugbyman_attacker.get_pos_x()>1:
                self.game.get_ball().set_pos([rugbyman_attacker.get_pos_x()-1,rugbyman_attacker.get_pos_y()])
            else:
                self.game.get_ball().set_pos([rugbyman_attacker.get_pos_x()+1,rugbyman_attacker.get_pos_y()])
        
        
    def charging(self,rugbyman_attacker,rugbyman_defender,possible_moves):
        """
        This function resolves the charging action between two rugbyman.

        Takes in arguments the attacking rugbyman, the defending rugbyman and the list of possible moves for the attacker

        Returns the attacking rugbyman if the charge was succesfull, False otherwise
        """

        #The condition is >=1 because once the attacker win, he has to be able to move past the defender 
        
        if rugbyman_attacker.get_moves_left()- tools.norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>=1:
            print("Red Player has to choose his card")
            c_red=self.choose_cards(self.game.get_player_red())
            self.graphique.draw_board(self.game)

            print("Blue Player has to choose his card")
            c_blue=self.choose_cards(self.game.get_player_blue())

            print("Red chose :"+str(c_red))
            print("Blue chose :"+str(c_blue))

            if rugbyman_attacker.get_color()==Color.RED:
                c_attacker=c_red
                c_defender=c_blue
            else:
                c_attacker=c_blue
                c_defender=c_red

            #If the attacker wins the charge
            if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus():
                self.attacker_win_charge(rugbyman_attacker,rugbyman_defender,possible_moves)          
            else :
                self.defender_win_charge(rugbyman_attacker,rugbyman_defender,possible_moves)
                
        else:
            print("You don't have enough move points left to charge this rugbyman")
            return False

    
    def choose_cards(self, player):

        """
        The function forces the player to choose a valid card and returns the number of the chosen card while
        updating the player's deck

        Takes in argument the player who has to choose a card

        Returns the number of the chosen card
        """
        
        #We draw the cards
        self.graphique.draw_cards(player)
        
        #is_card_returned is a boolean saying if the chosen card is already picked 
        is_card_returned=True

        active_cards=player.get_deck_int()
        pos,cond=self.graphique.get_hitbox_on_click()


        #The following is to make sure the player clicks on a card that is in 
        #his deck Meaning it is not already played

        while pos==False :

            self.graphique.draw_cards(player)
            pos,cond=self.graphique.get_hitbox_on_click()

        if player.get_color()==Color.RED:
            return self.red_choose_card(player,is_card_returned,pos,active_cards)

        if player.get_color()==Color.BLUE:
            return self.blue_choose_card(player,is_card_returned,pos,active_cards)
    
    def red_choose_card(self,player,is_card_returned,pos,active_cards):
        print("Red player Chooses his cards")

        while is_card_returned: #the following should be reconstructed better 

            while pos[1]>=(Constants.number_of_columns+2)//2 or pos[0]<2 or pos[0]>Constants.number_of_rows-1: 
                print("Please Click on a card")

                pos,cond=self.graphique.get_hitbox_on_click()
    
                while pos==False :
                    self.graphique.draw_cards(player)
                    pos,cond=self.graphique.get_hitbox_on_click()

            if pos[0]<(Constants.number_of_rows+2)//2:
                card_number=pos[1]//2+1

            else :
                card_number=pos[1]//2+4

            if card_number in active_cards:
                player.choose_card(cards.convert_int_to_card(card_number))
                is_card_returned=False
            else :
                print("You can't choose this card")
                pos,cond=self.graphique.get_hitbox_on_click()
        return card_number
    
    def blue_choose_card(self,player,is_card_returned,pos,active_cards):
        print("Blue player Chooses his cards")

        while is_card_returned:
            while pos[1]<=(Constants.number_of_columns+2)//2 or pos[0]<2 or pos[0]>Constants.number_of_rows-1: 
                print("Please Click on a card")
                pos,cond=self.graphique.get_hitbox_on_click()
                while pos==False :
                    self.graphique.draw_cards(player)
                    pos,cond=self.graphique.get_hitbox_on_click()
            if pos[0]<(Constants.number_of_rows+2)//2:
                card_number=(pos[1]+1)//2-3
            else :
                card_number=(pos[1]+1)//2
            if card_number in active_cards:
                player.choose_card(cards.convert_int_to_card(card_number))
                is_card_returned=False
            else :
                print("You can't choose this card")
                pos,cond=self.graphique.get_hitbox_on_click()
                while pos==False :
                    self.graphique.draw_cards(player)
                    pos,cond=self.graphique.get_hitbox_on_click()
        return card_number


    def tackling(self,rugbyman_attacker, rugbyman_defender,possible_moves):
        
        print("Players have to choose their cards")
        if self.game.is_rugbyman_on_ball()==rugbyman_defender:
            print("Red Player has to choose his card")
            c_red=self.choose_cards(self.game.get_player_red())
            print("Blue Player has to choose his card")
            self.graphique.draw_board(self.game)
            c_blue=self.choose_cards(self.game.get_player_blue())

            print("Red chose :"+str(c_red))
            print("Blue chose :"+str(c_blue))

            if rugbyman_attacker.get_color()==Color.RED:
                c_attacker=c_red
                c_defender=c_blue
            else:
                c_attacker=c_blue
                c_defender=c_red

            #If the attacker wins the tackle
            if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus():
                self.attacker_wins_tackle(rugbyman_attacker,rugbyman_defender,c_attacker,c_defender)
            else :
                rugbyman_attacker.set_KO()
            
            #If the rugbyman doing the tackling was far from the the defender
            if tools.norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>1:
                self.attacker_far_from_defender(rugbyman_attacker,rugbyman_defender,possible_moves)



            return rugbyman_attacker 
        else :
            print("You can only tackle the rugbyman with the ball")
            return False

    def attacker_wins_tackle(self,rugbyman_attacker,rugbyman_defender,c_attacker,c_defender):   
        rugbyman_defender.set_KO()
        rugbyman_defender.set_possesion(False)
        
        if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus()+1:
            print("Perfect tackle, the attacker keeps the ball ")
            self.game.get_ball().set_pos(rugbyman_attacker.get_pos())
            rugbyman_attacker.set_possesion(True)

        else :
            if rugbyman_defender.get_color()==Color.RED:
                    if rugbyman_defender.get_pos_y()>0:
                        self.game.get_ball().set_pos([rugbyman_defender.get_pos_x(),rugbyman_defender.get_pos_y()-1])
                    else:
                        if rugbyman_defender.get_pos_x()>0:
                            self.game.get_ball().set_pos([rugbyman_defender.get_pos_x()-1,rugbyman_defender.get_pos_y()])
                        else:
                            self.game.get_ball().set_pos([rugbyman_defender.get_pos_x()+1,rugbyman_defender.get_pos_y()])
            else:
                if rugbyman_defender.get_pos_y()<Constants.number_of_columns :
                    self.game.get_ball().set_pos([rugbyman_defender.get_pos_x(),rugbyman_defender.get_pos_y()+1])
                else:
                    if rugbyman_defender.get_pos_x()>0:
                        self.game.get_ball().set_pos([rugbyman_defender.get_pos_x()-1,rugbyman_defender.get_pos_y()])
                    else:
                        self.game.get_ball().set_pos([rugbyman_defender.get_pos_x()+1,rugbyman_defender.get_pos_y()])
            rugbyman_attacker.set_possesion(False)


    def action_rugbyman(self,rugbyman,possible_moves):
        """
        This function resolves an action that can be tackling, charging or simply moving depending on the situation 

        Takes in arguments the rugbyman that is doing the action and the list of possible moves for this rugbyman

        Returns the rugbyman if the action was succesfull, False otherwise
        """

        pos,cond = self.graphique.get_hitbox_on_click()
        possible_moves_without_scope_and_bool=[[k[0],k[1]] for k in possible_moves]

        if pos in possible_moves_without_scope_and_bool:
            i=possible_moves_without_scope_and_bool.index(pos)
            if possible_moves[i][3]:
                return self.move_rugbyman(pos,rugbyman,possible_moves[i][2])
            else :
                
                if self.game.is_rugbyman_on_ball()==rugbyman:
                    return self.charging(rugbyman,self.game.which_rugbyman_in_pos(pos),possible_moves)
                elif self.game.get_ball().get_pos()==pos:
                    return self.tackling(rugbyman,self.game.which_rugbyman_in_pos(pos),possible_moves) 
                else :
                    print("You can only tackle the rugbyman with the ball")  
                    return False
        else :
            print("You can't move to this position")
            return False
    

            
    def available_backward_pass( self ):

        """
        This function returns the list of available position for a backward pass for the rugbyman on the ball
        """

        rugbyman=self.game.is_rugbyman_on_ball()

        assert rugbyman != False, "There is no rugbyman on the ball"

        available = []

        current_x = rugbyman.get_pos_x()
        current_y = rugbyman.get_pos_y()

        pass_scope = Constants.back_pass_scope

        if rugbyman.get_color() is Color.RED:
            for x in range(current_x - pass_scope, current_x + pass_scope+1):
                for y in range( current_y - pass_scope, current_y):
                    if self.game.is_position_correct(x, y):
                        available.append([x, y])

        if rugbyman.get_color() is Color.BLUE:
            for x in range(current_x - pass_scope, current_x + pass_scope+1):
                for y in range( current_y +1, current_y+pass_scope+1):
                    if self.game.is_position_correct(x, y):
                        available.append([x, y])

        return available

    def available_forward_pass( self):
        """
        This function returns the list of available position for a forward pass for the rugbyman on the ball
        """

        rugbyman=self.game.is_rugbyman_on_ball()
        assert rugbyman != False, "There is no rugbyman on the ball"

        available = []

        current_x = rugbyman.get_pos_x()
        current_y = rugbyman.get_pos_y()

        pass_scope = Constants.forward_pass_scope

        cond = True
        
        if rugbyman.get_color() is Color.BLUE:
            for rugbyman in self.game.get_player_turn().get_rugbymen():
                if rugbyman.get_pos_y()<current_y:
                    cond = False

            if cond :
                for x in range(current_x - pass_scope, current_x + pass_scope+1):
                    for y in range( current_y - pass_scope, current_y):
                        if self.game.is_position_correct(x, y):
                            available.append([x, y])

        if rugbyman.get_color() is Color.RED:
            for rugbyman in self.game.get_player_turn().get_rugbymen():
                if rugbyman.get_pos_y()>current_y:
                    cond = False
            if cond :
                for x in range(current_x - pass_scope, current_x + pass_scope+1):
                    for y in range( current_y +1, current_y+pass_scope+1):
                        if self.game.is_position_correct(x, y):
                            available.append([x, y])

        return available

    def available_pass(self):
        rugbyman=self.game.is_rugbyman_on_ball()
        return self.available_forward_pass( )+self.available_backward_pass( )

    def make_pass(self,possible_passes):
        pos,cond=self.graphique.get_hitbox_on_click()
        catched_cond=False


        if pos in possible_passes:
            #former_owner is the rugbyman who had the ball before the pass
            former_owner=self.game.is_rugbyman_on_ball()

            #If the pass is backward (meaning it can be catched)
            if (former_owner.get_color() is Color.RED
                and pos[1] < former_owner.get_pos_y()):
                catched_cond=self.red_backward_pass_catch(pos,former_owner)
                            
            #Same with the blue the only difference is that the receiver has to be above the thrower
            if (former_owner.get_color() is Color.BLUE
                and pos[1] > former_owner.get_pos_y()):
                catched_cond=self.blue_backward_pass_catch(pos,former_owner)
        
            if catched_cond==True:
                return catched_cond
            
            self.game.is_rugbyman_on_ball().set_possesion(False)
            self.game.get_ball().set_pos(pos)

            if self.game.is_rugbyman_on_ball()!=False:
                self.game.is_rugbyman_on_ball().set_possesion(True)
    
    def red_backward_pass_catch(self,pos,former_owner):
        #For each rugbyman of the opposing team we have to check if they can catch the ball
        min=100
        for rugbyman in self.game.get_player_blue().get_rugbymen():
            #We check if the rugbyman is in the right position to catch the ball
            if (rugbyman.get_pos_y() <= former_owner.get_pos_y() 
                and rugbyman.get_pos_y() >= pos[1]
                and rugbyman.get_KO()==0):

                #Receiver and adversary are both above the thrower or both under 
                #This condition this necessary since the norm alone isnt enough
                if (rugbyman.get_pos_x() -former_owner.get_pos_x())*(pos[0] -former_owner.get_pos_x())>=0:

                    #We check if the rugbyman is closer to the ball than the former owner
                    if (tools.norm(rugbyman.get_pos(),former_owner.get_pos())<tools.norm(former_owner.get_pos(),pos)
                        and min>tools.norm(rugbyman.get_pos(),former_owner.get_pos())):   
                        rugbyman_closer=rugbyman
                        min=tools.norm(rugbyman.get_pos(),former_owner.get_pos())
        if min<100:
            rugbyman_closer.set_possesion(True)
            former_owner.set_possesion(False)
            self.game.get_ball().set_carrier(rugbyman_closer)
            self.game.get_ball().set_pos(rugbyman_closer.get_pos())
            return True

    def blue_backward_pass_catch(self,pos,former_owner):
        min=100
        for rugbyman in self.game.get_player_red().get_rugbymen():
            if (rugbyman.get_pos_y() >= former_owner.get_pos_y() 
                and rugbyman.get_pos_y() <= pos[1]
                and rugbyman.get_KO()==0):
                #ensure there on the same side of the passing position set
                if (rugbyman.get_pos_x() -former_owner.get_pos_x())*(pos[0] -former_owner.get_pos_x())>=0:
                    
                    if (tools.norm(rugbyman.get_pos(),former_owner.get_pos())<tools.norm(former_owner.get_pos(),pos)
                        and min>tools.norm(rugbyman.get_pos(),former_owner.get_pos())):   
                        rugbyman_closer=rugbyman
                        min=tools.norm(rugbyman.get_pos(),former_owner.get_pos())
        if min<100:
            rugbyman_closer.set_possesion(True)
            former_owner.set_possesion(False)
            self.game.get_ball().set_carrier(rugbyman_closer)
            self.game.get_ball().set_pos(rugbyman_closer.get_pos())
            return True





class ActionMiniMax(Action):
    def __init__(self, game, graphique):
        super().__init__(game, graphique)

    def action_rugbyman_AI_defending(self,rugbyman,possible_moves):
        """
        This function resolves an action that can be tackling, charging or simply moving depending on the situation 

        Takes in arguments the rugbyman that is doing the action and the list of possible moves for this rugbyman

        Returns the rugbyman if the action was succesfull, False otherwise
        """

        pos,cond = self.graphique.get_hitbox_on_click()
        possible_moves_without_scope_and_bool=[[k[0],k[1]] for k in possible_moves]

        if pos in possible_moves_without_scope_and_bool:
            i=possible_moves_without_scope_and_bool.index(pos)
            if possible_moves[i][3]:
                return self.move_rugbyman(pos,rugbyman,possible_moves[i][2])
            else :
                
                if self.game.is_rugbyman_on_ball()==rugbyman:
                    return self.charging_AI_blue_defending(rugbyman,self.game.which_rugbyman_in_pos(pos),possible_moves)
                elif self.game.get_ball().get_pos()==pos:
                    return self.tackling_AI_defending(rugbyman,self.game.which_rugbyman_in_pos(pos),possible_moves) 
                else :
                    print("You can only tackle the rugbyman with the ball")  
                    return False
        else :
            print("You can't move to this position")
            return False
    

    def charging_AI_blue_defending(self,rugbyman_attacker,rugbyman_defender,possible_moves):
        """
        This function resolves the charging action between two rugbyman.

        Takes in arguments the attacking rugbyman, the defending rugbyman and the list of possible moves for the attacker

        Returns the attacking rugbyman if the charge was succesfull, False otherwise
        """

        #The condition is >=1 because once the attacker win, he has to be able to move past the defender 
        
        if rugbyman_attacker.get_moves_left()- tools.norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>=1:
            print("Red Player has to choose his card")
            c_red=self.choose_cards(self.game.get_player_red())
            self.graphique.draw_board(self.game)

            print("Blue Player has to choose his card")
            c_blue=self.choose_cards_AI(self.game.get_player_blue())


            print("Red chose :"+str(c_red))
            print("Blue chose :"+str(c_blue))

            if rugbyman_attacker.get_color()==Color.RED:
                c_attacker=c_red
                c_defender=c_blue
            else:
                c_attacker=c_blue
                c_defender=c_red

            #If the attacker wins the charge
            if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus():
                self.attacker_win_charge(rugbyman_attacker,rugbyman_defender,possible_moves)          
            else :
                self.defender_win_charge(rugbyman_attacker,rugbyman_defender,possible_moves)
                
        else:
            print("You don't have enough move points left to charge this rugbyman")
            return False


    def undo_move_rugbyman( self,former_rugbyman_pos,former_ball_pos,rugbyman,cost):
            ball=self.game.get_ball()
            rugbyman.set_pos(former_rugbyman_pos)
            rugbyman.set_move_left(cost)
            
            if former_rugbyman_pos==former_ball_pos:
                ball.set_pos(former_rugbyman_pos)
                ball.set_carrier(rugbyman)
                rugbyman.set_possesion(True)
            else :
                rugbyman.set_possesion(False)

    def make_pass_AI(self,pos):

        #former_owner is the rugbyman who had the ball before the pass
        former_owner=self.game.is_rugbyman_on_ball()
        #print(former_owner)
        #It is useless to send the ball to an adversary
        if (self.game.which_rugbyman_in_pos(pos)!=False 
            and self.game.which_rugbyman_in_pos(pos).get_color()!=former_owner.get_color()):
            return False
        
        
        
        #If the pass is backward (meaning it can be catched)
        if (former_owner.get_color() is Color.RED
            and pos[1] < former_owner.get_pos_y()):

            #For each rugbyman of the opposing team we have to check if they can catch the ball
            min=100
            for rugbyman in self.game.get_player_blue().get_rugbymen():
                #We check if the rugbyman is in the right position to catch the ball
                if (rugbyman.get_pos_y() < former_owner.get_pos_y() 
                    and rugbyman.get_pos_y() >= pos[1]
                    and rugbyman.get_KO()==0):

                    #Receiver and adversary are both above the thrower or both under 
                    #This condition this necessary since the norm alone isnt enough
                    if (rugbyman.get_pos_x() -former_owner.get_pos_x())*(pos[0] -former_owner.get_pos_x())>=0:

                        #We check if the rugbyman is closer to the ball than the former owner
                        if (tools.norm(rugbyman.get_pos(),pos)<tools.norm(former_owner.get_pos(),pos)
                            and min>tools.norm(rugbyman.get_pos(),former_owner.get_pos())):
                            return False
        #Same with the blue the only difference is that the receiver has to be above the thrower
        if (former_owner.get_color() is Color.BLUE
            and pos[1] > former_owner.get_pos_y()):
            min=100
            for rugbyman in self.game.get_player_red().get_rugbymen():
                if (rugbyman.get_pos_y() > former_owner.get_pos_y() 
                    and rugbyman.get_pos_y() <= pos[1]
                    and rugbyman.get_KO()==0):
                    #ensure there on the same side of the passing position set
                    if (rugbyman.get_pos_x() -former_owner.get_pos_x())*(pos[0] -former_owner.get_pos_x())>=0:
                        
                        if (tools.norm(rugbyman.get_pos(),pos)<tools.norm(former_owner.get_pos(),pos)
                            and min>tools.norm(rugbyman.get_pos(),former_owner.get_pos())):   
                                return False
        
        
        self.game.is_rugbyman_on_ball().set_possesion(False)
        self.game.get_ball().set_pos(pos)

        if self.game.is_rugbyman_on_ball()!=False:
            self.game.is_rugbyman_on_ball().set_possesion(True)

    def undo_pass_AI(self,former_ball_pos,former_owner):
        if self.game.is_rugbyman_on_ball()!=False:
            self.game.is_rugbyman_on_ball().set_possesion(False)
        
        self.game.get_ball().set_pos(former_ball_pos)
        former_owner.set_possesion(True)
        self.game.get_ball().set_carrier(former_owner)    

    def tackling_AI_defending(self,rugbyman_attacker, rugbyman_defender,possible_moves):
        
        print("Players have to choose their cards")
        if self.game.is_rugbyman_on_ball()==rugbyman_defender:
            print("Red Player has to choose his card")
            c_red=self.choose_cards(self.game.get_player_red())
            print("Blue Player has to choose his card")
            self.graphique.draw_board(self.game)
            c_blue=self.choose_cards_AI(self.game.get_player_blue())

            print("Red chose :"+str(c_red))
            print("Blue chose :"+str(c_blue))

            if rugbyman_attacker.get_color()==Color.RED:
                c_attacker=c_red
                c_defender=c_blue
            else:
                c_attacker=c_blue
                c_defender=c_red

            #If the attacker wins the tackle
            if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus():
                self.attacker_wins_tackle(rugbyman_attacker,rugbyman_defender,c_attacker,c_defender)
            else :
                rugbyman_attacker.set_KO()
            
            #If the rugbyman doing the tackling was far from the the defender
            if tools.norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>1:
                self.attacker_far_from_defender(rugbyman_attacker,rugbyman_defender,possible_moves)



            return rugbyman_attacker 
        else :
            print("You can only tackle the rugbyman with the ball")
            return False
    
    def  action_rugbyman_AI(self,rugbyman_attacker,rugbyman_defender,possible_moves):
        if self.game.is_rugbyman_on_ball()==rugbyman_attacker:
            return False # Not working yet
            return self.charging_AI(rugbyman_attacker,rugbyman_defender,possible_moves)
        elif self.game.get_ball().get_pos()==rugbyman_defender.get_pos():
            return self.tackling_AI(rugbyman_attacker,rugbyman_defender,possible_moves) 
        return False

    def charging_AI(self,rugbyman_attacker, rugbyman_defender,possible_moves):
        """
        This charging function is meant to be used by the minimax algorithm it does not do anything
        """
        #the condition is >=1 because once he is on him he has to be able to move
        if rugbyman_attacker.get_moves_left()- tools.norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>=1:
            
            #To simplify the logical choice is always the best card (at small depth)
            #Optimization could be made here by making the AI choose the smallest card enabling him to win the charge
            c_red=max(self.game.get_player_red().get_deck_int()) 
            c_blue= max(self.game.get_player_blue().get_deck_int())

            if rugbyman_attacker.get_color()==Color.RED:
                c_attacker=c_red
                c_defender=c_blue
            else:
                c_attacker=c_blue
                c_defender=c_red

            #If the attacker wins the charge
            if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus():
                #Defender is KO
                rugbyman_defender.set_KO()

                #He loses the ball and attacker retreives it
                rugbyman_defender.set_possesion(False)
                self.game.get_ball().set_pos(rugbyman_defender.get_pos()) #A bit useless here since the ball was already in the defender position
                rugbyman_attacker.set_possesion(True)

                #Rugbyman attacker is on defender position we then actualize his position and move left
                rugbyman_attacker.set_pos(rugbyman_defender.get_pos())
                for move in possible_moves:
                    if move[:2]==rugbyman_defender.get_pos():
                        rugbyman_attacker.set_move_left(move[2])
                
                #Here it is hard to choose the best move as it is outside the minimax evaluation yet we will pick the best move still
                possible_moves=self.game.available_move_position(rugbyman_attacker)
                award=-10000
                for move in possible_moves:
                    rugbyman_attacker.set_pos(move[:2])
                    if award<self.game.award_function(Game.get_player_turn()):
                        award=self.game.award_function(Game.get_player_turn())
                        best_move=move
                    rugbyman_attacker.set_pos(rugbyman_defender.get_pos())
                rugbyman_attacker.set_pos(best_move[:2])
                return True 
                
            else : 
                #if the attacker has more chance of losing the battle then it is not worth it
                return False
        else:
            return False
        
    def tackling_AI(self,rugbyman_attacker, rugbyman_defender,possible_moves):


        if self.game.is_rugbyman_on_ball()==rugbyman_defender:
            
            print("Red Player has to choose his card")
            c_blue=self.choose_cards_AI(self.game.get_player_blue())
            
            c_red=self.choose_cards(self.game.get_player_red())

            print(rugbyman_attacker.get_color())
            if rugbyman_attacker.get_color()==Color.RED:
                c_attacker=c_red
                c_defender=c_blue
            else:
                c_attacker=c_blue
                c_defender=c_red

            #If the attacker wins the charge
            if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus():
                rugbyman_defender.set_KO()
                rugbyman_defender.set_possesion(False)

                if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus()+1:
                    self.game.get_ball().set_pos(rugbyman_attacker.get_pos())
                
                if rugbyman_defender.get_color()==Color.RED:
                        if rugbyman_defender.get_pos_y()>0:
                            self.game.get_ball().set_pos([rugbyman_defender.get_pos_x(),rugbyman_defender.get_pos_y()-1])
                        else:
                            if rugbyman_defender.get_pos_x()>0:
                                self.game.get_ball().set_pos([rugbyman_defender.get_pos_x()-1,rugbyman_defender.get_pos_y()])
                            else:
                                self.game.get_ball().set_pos([rugbyman_defender.get_pos_x()+1,rugbyman_defender.get_pos_y()])
                else:
                    if rugbyman_defender.get_pos_y()<Constants.number_of_columns :
                        self.game.get_ball().set_pos([rugbyman_defender.get_pos_x(),rugbyman_defender.get_pos_y()+1])
                    else:
                        if rugbyman_defender.get_pos_x()>0:
                            self.game.get_ball().set_pos([rugbyman_defender.get_pos_x()-1,rugbyman_defender.get_pos_y()])
                        else:
                            self.game.get_ball().set_pos([rugbyman_defender.get_pos_x()+1,rugbyman_defender.get_pos_y()])
                rugbyman_attacker.set_possesion(False)
            else :
                rugbyman_attacker.set_KO()
            
            #If the rugbyman doing the tackling was far from the the defender
            #We have to replace him so that the tackling makes sense 
            
            if tools.norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>1:
                min_norm=100
                for moves in possible_moves:
                    if tools.norm([moves[0],moves[1]],rugbyman_defender.get_pos())==1:
                        if (tools.norm([moves[0],moves[1]],rugbyman_attacker.get_pos())<min_norm
                            and moves[3]): #moves[3] ensure that the square is free
                        
                            min_norm=tools.norm([moves[0],moves[1]],rugbyman_attacker.get_pos())
                            new_attacker_pos=[moves[0],moves[1]]
                            new_attacker_cost=moves[2]
                if min_norm<100: #why not ???
                    rugbyman_attacker.set_pos(new_attacker_pos)
                    rugbyman_attacker.set_move_left(new_attacker_cost)

            if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus()+1:
                self.game.get_ball().set_pos(rugbyman_attacker.get_pos())
                self.game.get_ball().set_carrier(rugbyman_attacker)
                rugbyman_attacker.set_possesion(True)
            return True 
        else :
            rugbyman_attacker.set_KO()
        
    def choose_cards_AI(self,player):
        #We wait for the player to choose his cards
        card_number=max(player.get_deck_int())
        player.choose_card(cards.convert_int_to_card(max(player.get_deck_int())))
        
        return card_number

class ActionBot(Action):
    def __init__(self, game, graphique):
        super().__init__(game, graphique)
    
    def action_rugbyman_with_bot(self,rugbyman,possible_moves):
        pos,cond = self.graphique.get_hitbox_on_click()
        possible_moves_without_scope_and_bool=[[k[0],k[1]] for k in possible_moves]

        if pos in possible_moves_without_scope_and_bool:
            i=possible_moves_without_scope_and_bool.index(pos)
            if possible_moves[i][3]:
                return move_rugbyman(pos,rugbyman,self.game.get_ball(),possible_moves[i][2])
            else :
                
                if self.game.is_rugbyman_on_ball()==rugbyman:
                    return charging_bot(Graphique,Game,rugbyman,self.game.which_rugbyman_in_pos(pos),possible_moves)
                elif self.game.get_ball().get_pos()==pos:
                    return tackling_bot(Graphique,Game,rugbyman,self.game.which_rugbyman_in_pos(pos),possible_moves) 
                else :
                    print("You can only tackle the rugbyman with the ball")  
                    return False
        else :
            print("You can't move to this position")
            return False
    
    def action_rugbyman_bot(pos, rugbyman, Game, Graphique):
        possible_moves = Game.available_move_position(rugbyman)
        possible_moves_without_scope_and_bool = [[k[0],k[1]] for k in possible_moves]
        if pos in possible_moves_without_scope_and_bool:
            i=possible_moves_without_scope_and_bool.index(pos)
            if possible_moves[i][3]:
                return move_rugbyman(pos,rugbyman,Game.get_ball(),possible_moves[i][2])
            else :
                if Game.is_rugbyman_on_ball() == rugbyman:
                    return charging_bot(Graphique,Game,rugbyman,Game.which_rugbyman_in_pos(pos),possible_moves)
                elif Game.get_ball().get_pos() == pos:
                    return tackling_bot(Graphique,Game,rugbyman,Game.which_rugbyman_in_pos(pos),possible_moves) 
                else : 
                    return False
        else :
            return False
        
    def tackling_bot(self,rugbyman_attacker, rugbyman_defender,possible_moves):
        
        print("Players have to choose their cards")
        if self.game.is_rugbyman_on_ball()==rugbyman_defender:
            print("Red Player has to choose his card")
            c_red=ActionBot.draw_card_bot()
            print("Blue Player has to choose his card")
            self.graphique.draw_board(self.game)
            c_blue=self.choose_cards(self.graphique,self.game.get_player_blue())

            print("Red chose :"+str(c_red))
            print("Blue chose :"+str(c_blue))

            if rugbyman_attacker.get_color()==Color.RED:
                c_attacker=c_red
                c_defender=c_blue
            else:
                c_attacker=c_blue
                c_defender=c_red


            if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus():
                rugbyman_defender.set_KO()
                rugbyman_defender.set_possesion(False)

                if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus()+1:
                    self.game.get_ball().set_pos(rugbyman_attacker.get_pos())
                
                if rugbyman_defender.get_color()==Color.RED:
                        if rugbyman_defender.get_pos_y()>0:
                            self.game.get_ball().set_pos([rugbyman_defender.get_pos_x(),rugbyman_defender.get_pos_y()-1])
                        else:
                            if rugbyman_defender.get_pos_x()>0:
                                self.game.get_ball().set_pos([rugbyman_defender.get_pos_x()-1,rugbyman_defender.get_pos_y()])
                            else:
                                self.game.get_ball().set_pos([rugbyman_defender.get_pos_x()+1,rugbyman_defender.get_pos_y()])
                else:
                    if rugbyman_defender.get_pos_y()<Constants.number_of_columns :
                        self.game.get_ball().set_pos([rugbyman_defender.get_pos_x(),rugbyman_defender.get_pos_y()+1])
                    else:
                        if rugbyman_defender.get_pos_x()>0:
                            self.game.get_ball().set_pos([rugbyman_defender.get_pos_x()-1,rugbyman_defender.get_pos_y()])
                        else:
                            self.game.get_ball().set_pos([rugbyman_defender.get_pos_x()+1,rugbyman_defender.get_pos_y()])
                rugbyman_attacker.set_possesion(False)
            else :
                rugbyman_attacker.set_KO()
            
            #If the rugbyman doing the tackling was far from the the defender
            if tools.norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>1:
                min_norm=100
                for moves in possible_moves:
                    if tools.norm([moves[0],moves[1]],rugbyman_defender.get_pos())==1:
                        if (tools.norm([moves[0],moves[1]],rugbyman_attacker.get_pos())<min_norm
                            and moves[3]): #moves[3] ensure that the square is free
                        
                            min_norm=tools.norm([moves[0],moves[1]],rugbyman_attacker.get_pos())
                            new_attacker_pos=[moves[0],moves[1]]
                            new_attacker_cost=moves[2]
                if min_norm<100: #why not ???
                    rugbyman_attacker.set_pos(new_attacker_pos)
                    rugbyman_attacker.set_move_left(new_attacker_cost)

                if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus()+1:
                    print("Perfect tackle, the attacker keeps the ball ")
                    self.game.get_ball().set_pos(new_attacker_pos)
                    self.game.get_ball().set_carrier(rugbyman_attacker)
                    rugbyman_attacker.set_possesion(True)
            
            else :
                if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus()+1:
                    print("Perfect tackle, the attacker keeps the ball ")
                    self.game.get_ball().set_pos(rugbyman_attacker.get_pos())
                    self.game.get_ball().set_carrier(rugbyman_attacker)
                    rugbyman_attacker.set_possesion(True)

            return rugbyman_attacker 
        else :
            print("You can only tackle the rugbyman with the ball")
            return False

    def charging_bot(self,rugbyman_attacker, rugbyman_defender,possible_moves):
        #the condition is >=1 because once he is on him he has to be able to move
        if rugbyman_attacker.get_moves_left()- tools.norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>=1:
            print("Red Player has to choose his card")
            c_red=ActionBot.draw_card_bot()
            self.graphique.draw_board(self.game)
            print("Blue Player has to choose his card")
            c_blue=ActionBot.choose_cards(self.graphique,self.game.get_player_blue())

            print("Red chose :"+str(c_red))
            print("Blue chose :"+str(c_blue))
            if rugbyman_attacker.get_color() == Color.RED:
                c_attacker=c_red
                c_defender=c_blue
            else:
                c_attacker=c_blue
                c_defender=c_red

            #If the attacker wins the charge
            if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus():
                #Defender is KO
                rugbyman_defender.set_KO()

                #He loses the ball and attacker retreives it
                rugbyman_defender.set_possesion(False)
                self.game.get_ball().set_pos(rugbyman_defender.get_pos()) #A bit useless here since the ball was already in the defender position
                rugbyman_attacker.set_possesion(True)

                #Rugbyman attacker is on defender position we then actualize his position and move left
                rugbyman_attacker.set_pos(rugbyman_defender.get_pos())
                for move in possible_moves:
                    if move[:2]==rugbyman_defender.get_pos():
                        rugbyman_attacker.set_move_left(move[2])
                
                #We re-compute the list of possible moves for the attacker and make him move
                self.graphique.draw_board(Game)
                possible_moves=self.game.available_move_position(rugbyman_attacker)
                self.graphique.highlight_move(possible_moves)
                #This function forces the rugbyman to move
                self.move_rugbyman_after_succesfull_charging(rugbyman_attacker,self.game.get_ball(),possible_moves)
                
            else : 
                #If the defender wins the charge
                rugbyman_attacker.set_KO()
                
                #We then have to move the now lost ball to a new position 
                if rugbyman_attacker.get_color()==Color.RED:
                    if rugbyman_attacker.get_pos_y()>1:
                        #The first normal position (happens 90% of the time) is just putting the ball behind the attacker
                        self.game.get_ball().set_pos([rugbyman_attacker.get_pos_x(),rugbyman_attacker.get_pos_y()-1])
                    else:
                        
                        #If the attacker is on the edge of the board we put the ball on the side
                        if rugbyman_attacker.get_pos_x()>1:
                            self.game.get_ball().set_pos(rugbyman_attacker.get_pos()+[-1,0])
                        else:
                            self.game.get_ball().set_pos([rugbyman_attacker.get_pos_x()+1,rugbyman_attacker.get_pos_y()])
                else:
                    #Same but here the "behind" blue is towards the right 
                    if rugbyman_attacker.get_pos_y()<Constants.number_of_columns :
                        self.game.get_ball().set_pos([rugbyman_attacker.get_pos_x(),rugbyman_attacker.get_pos_y()-1])
                    else:
                        if rugbyman_attacker.get_pos_x()>1:
                            self.game.get_ball().set_pos([rugbyman_attacker.get_pos_x()-1,rugbyman_attacker.get_pos_y()])
                        else:
                            self.game.get_ball().set_pos([rugbyman_attacker.get_pos_x()+1,rugbyman_attacker.get_pos_y()])
                rugbyman_attacker.set_possesion(False)
                
                #If the rugbyman doing the charging was far from the the defender we have to replace it like he made 
                #the move one square by one square
                if tools.norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>1:
                    min_norm=100
                    #we iterate over the possible moves of the attacker (moves where he could have been if he took the time to move 
                    # his rugbyman one square by one square)
                    for move in possible_moves:
                        
                        #The relocation has to be close to the defender
                        if tools.norm(move[:2],rugbyman_defender.get_pos())==1:
                            #The closest square is the natural choice
                            if tools.norm(move[:2],rugbyman_attacker.get_pos())<min_norm:

                                min_norm=tools.norm([move[0],move[1]],rugbyman_attacker.get_pos())
                                new_attacker_pos=[move[0],move[1]]
                                new_attacker_cost=move[2]
                    if min_norm<100:
                        rugbyman_attacker.set_pos(new_attacker_pos)
                        rugbyman_attacker.set_move_left(new_attacker_cost)
            return rugbyman_attacker 
        else:
            print("You don't have enough move points left to charge this rugbyman")
            return False

class ActionRL(Action):
    def RL_tackling(self, rugbyman_attacker, rugbyman_defender,Possible_moves):
        """
        Effectue un tacle demandé par le bot Deep Q Learning.
        Contient en partie des élements du bot de Félix.
        """
        game_RL = self.game
        if game_RL.is_rugbyman_on_ball()==rugbyman_defender:
            
            c_blue= 1
            c_red=max(game_RL.get_player_red().get_deck_int())


            if rugbyman_attacker.get_color()==Color.RED:
                c_attacker=c_red
                c_defender=c_blue
            else:
                c_attacker=c_blue
                c_defender=c_red

            #If the attacker wins the charge
            if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus():
                rugbyman_defender.set_KO()
                rugbyman_defender.set_possesion(False)

                if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus()+1:
                    game_RL.get_ball().set_pos(rugbyman_attacker.get_pos())
                
                if rugbyman_defender.get_color()==Color.RED:
                        if rugbyman_defender.get_pos_y()>0:
                            game_RL.get_ball().set_pos([rugbyman_defender.get_pos_x(),rugbyman_defender.get_pos_y()-1])
                        else:
                            if rugbyman_defender.get_pos_x()>0:
                                game_RL.get_ball().set_pos([rugbyman_defender.get_pos_x()-1,rugbyman_defender.get_pos_y()])
                            else:
                                game_RL.get_ball().set_pos([rugbyman_defender.get_pos_x()+1,rugbyman_defender.get_pos_y()])
                else:
                    if rugbyman_defender.get_pos_y()<Constants.number_of_columns :
                        game_RL.get_ball().set_pos([rugbyman_defender.get_pos_x(),rugbyman_defender.get_pos_y()+1])
                    else:
                        if rugbyman_defender.get_pos_x()>0:
                            game_RL.get_ball().set_pos([rugbyman_defender.get_pos_x()-1,rugbyman_defender.get_pos_y()])
                        else:
                            game_RL.get_ball().set_pos([rugbyman_defender.get_pos_x()+1,rugbyman_defender.get_pos_y()])
                rugbyman_attacker.set_possesion(False)
            else :
                return False 
            if tools.norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>1:
                min_norm=100
                for moves in Possible_moves:
                    if tools.norm([moves[0],moves[1]],rugbyman_defender.get_pos())==1:
                        if (tools.norm([moves[0],moves[1]],rugbyman_attacker.get_pos())<min_norm
                            and moves[3]): #moves[3] ensure that the square is free
                        
                            min_norm=tools.norm([moves[0],moves[1]],rugbyman_attacker.get_pos())
                            new_attacker_pos=[moves[0],moves[1]]
                            new_attacker_cost=moves[2]
                if min_norm<100: #why not ???
                    rugbyman_attacker.set_pos(new_attacker_pos)
                    rugbyman_attacker.set_move_left(new_attacker_cost)

            if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus()+1:
                game_RL.get_ball().set_pos(rugbyman_attacker.get_pos())
                game_RL.get_ball().set_carrier(rugbyman_attacker)
                rugbyman_attacker.set_possesion(True)
            return True 
        else :
            return False
        

    def RL_charging(self, rugbyman_attacker, rugbyman_defender,Possible_moves):
        """
        This charging function is meant to be used by the minimax algorithm it does not do anything
        """
        game_RL = self.game
        #the condition is >=1 because once he is on him he has to be able to move
        if rugbyman_attacker.get_moves_left()- tools.norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>=1:
            
            #To simplify the logical choice is always the best card (at small depth)
            #Optimization could be made here by making the AI choose the smallest card enabling him to win the charge
            c_red=max(game_RL.get_player_red().get_deck_int()) 
            c_blue= max(game_RL.get_player_blue().get_deck_int())

            if rugbyman_attacker.get_color()==Color.RED:
                c_attacker=c_red
                c_defender=c_blue
            else:
                c_attacker=c_blue
                c_defender=c_red

            #If the attacker wins the charge
            if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus():
                #Defender is KO
                rugbyman_defender.set_KO()

                #He loses the ball and attacker retreives it
                rugbyman_defender.set_possesion(False)
                game_RL.get_ball().set_pos(rugbyman_defender.get_pos()) #A bit useless here since the ball was already in the defender position
                rugbyman_attacker.set_possesion(True)

                #Rugbyman attacker is on defender position we then actualize his position and move left
                rugbyman_attacker.set_pos(rugbyman_defender.get_pos())
                for move in Possible_moves:
                    if move[:2]==rugbyman_defender.get_pos():
                        rugbyman_attacker.set_move_left(move[2])
                
                #Here it is hard to choose the best move as it is outside the minimax evaluation yet we will pick the best move still
                Possible_moves=game_RL.available_move_position(rugbyman_attacker)
                award=-10000
                for move in Possible_moves:
                    rugbyman_attacker.set_pos(move[:2])
                    if award<game_RL.award_function(game_RL.get_player_turn()):
                        award=game_RL.award_function(game_RL.get_player_turn())
                        best_move=move
                    rugbyman_attacker.set_pos(rugbyman_defender.get_pos())
                rugbyman_attacker.set_pos(best_move[:2])
                return True 
                
            else : 
                #if the attacker has more chance of losing the battle then it is not worth it
                return False
        else:
            return False

    def RL_action_rugbyman(self, rugbyman_attacker,rugbyman_defender,Possible_moves):
        """
        Effectue une action de rugbyman demandée par le bot Deep Q Learning dans le cas où il y a un ennemi. 
        Si un ennemi est dans la nouvelle case, c'est un tacle si le rugbyman n'a pas la balle, une charge sinon. 
        """
        game = self.game
        if game.is_rugbyman_on_ball() == rugbyman_attacker:
            return self.RL_charging(rugbyman_attacker,rugbyman_defender,Possible_moves)

        elif game.get_ball().get_pos() == rugbyman_defender.get_pos():
            return self.RL_tackling(rugbyman_attacker,rugbyman_defender,Possible_moves) 
        return False