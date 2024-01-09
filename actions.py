import rugbymen
import front
import random
from color import Color
import players
import game
import ball
from constants import *
import cards   
import enum

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


def positions_rugbymen_player(placement_order, Graphique):

    i = 0
    n_rugbymen = len(placement_order)
    R = [None] * n_rugbymen 
    L_pos=[]
    Noms = list(placement_order.keys())  
    color=placement_order[Noms[0]].get_color()

    
    for i in range(n_rugbymen):
        placement_order[Noms[i]].set_pos_x(i+1)
        if color == Color.RED:
            placement_order[Noms[i]].set_pos_y(random.randint(1, 5))
        else:
            placement_order[Noms[i]].set_pos_y(7)

        R[i]=placement_order[Noms[i]]
        front.Graphique.display_rugbyman(Graphique,R[i])
    return R
    
    front.pygame.display.flip()
    while i < n_rugbymen:
        # The Color.split(".")[-1] is for the color to display as intended
        print( str(color).split(".")[-1] + " Player, Choose the position of the " + Noms[i])
        # Fonction de la classe graphique qui renvoie une liste de la forme [i,j] avec i et j les colonnes et lignes de la case cliquée
        pos,cond = front.Graphique.get_hitbox_on_click(Graphique)

        #This step is necessary to ensure that player can resize the screen
        while pos==False:
            pos,cond = front.Graphique.get_hitbox_on_click(Graphique)

        if pos in L_pos:
            cond_pos_already_taken = True
            while cond_pos_already_taken:
                print("The position chosen is already taken, re choose the position")
                pos,cond = front.Graphique.get_hitbox_on_click(Graphique)
                if not pos in L_pos:
                    cond_pos_already_taken = False

        if (color == Color.RED 
            and (pos[1] > Constants.number_of_columns // 2
            or pos[1]==0)):  # Red characters should be placed on the left
            cond_RED = True
            while cond_RED:
                print("The position isn't correct, the red team is suppose to be on the left of the field")
                pos,cond = front.Graphique.get_hitbox_on_click(Graphique)
                if pos[1] < Constants.number_of_columns // 2+1 and pos[1]!=0:
                    cond_RED = False

        if (color == Color.BLUE 
            and (pos[1] <= Constants.number_of_columns // 2+1
            or pos[1]==Constants.number_of_columns+1)):  # Blue characters should be placed on the right
            cond_Blue = True
            while cond_Blue:
                print("The position isn't correct, the blue team is suppose to be on the right, re choose the position")
                pos,cond = front.Graphique.get_hitbox_on_click(Graphique)
                if pos[1] > Constants.number_of_columns // 2+1 and pos[1]!=Constants.number_of_columns+1:
                    cond_Blue = False
        
        #Toutes les conditions ont été vérifiées, on peut enregistrer les informations
        placement_order[Noms[i]].set_pos(pos)
        Graphique.display_rugbyman(placement_order[Noms[i]])  # Display the newly placed rugbymen on the board
        R[i] =  placement_order[Noms[i]]
        L_pos.append(pos)
        front.pygame.display.flip()
        i += 1
    return R

def move_rugbyman_after_succesfull_charging( Graphique,rugbyman,ball,Possible_moves):
        """
        Move the rugbyman
        
        """
        while True:
            pos,cond=front.Graphique.get_hitbox_on_click(Graphique)

            Possible_moves_without_scope_and_bool = [[k[0],k[1]] for k in Possible_moves]
            if pos in Possible_moves_without_scope_and_bool:
                i=Possible_moves_without_scope_and_bool.index(pos)
                if Possible_moves[i][3]:
                    return move_rugbyman(pos,rugbyman,ball,Possible_moves[i][2])
                else :
                    print("You can't move to this position")
            

def move_rugbyman( pos,rugbyman,ball,cost):
        
        
        if rugbyman.get_possesion():
            ball.set_pos(pos)
        
        rugbyman.set_pos(pos)
        rugbyman.set_move_left(cost)

        if rugbyman.get_pos()==ball.get_pos():
            ball.set_carrier(rugbyman)
            rugbyman.set_possesion(True)
            
        return rugbyman
        
def charging(Graphique,Game,rugbyman_attacker, rugbyman_defender,Possible_moves):
    #the condition is >=1 because once he is on him he has to be able to move
    if rugbyman_attacker.get_moves_left()- norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>=1:
        print("Red Player has to choose his card")
        c_red=choose_cards(Graphique,Game.get_player_red())
        Graphique.draw_board(Game)
        print("Blue Player has to choose his card")
        c_blue=choose_cards(Graphique,Game.get_player_blue())

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
            #Defender is KO
            rugbyman_defender.set_KO()

            #He loses the ball and attacker retreives it
            rugbyman_defender.set_possesion(False)
            Game.get_ball().set_pos(rugbyman_defender.get_pos()) #A bit useless here since the ball was already in the defender position
            rugbyman_attacker.set_possesion(True)

            #Rugbyman attacker is on defender position we then actualize his position and move left
            rugbyman_attacker.set_pos(rugbyman_defender.get_pos())
            for move in Possible_moves:
                if move[:2]==rugbyman_defender.get_pos():
                    rugbyman_attacker.set_move_left(move[2])
            
            #We re-compute the list of possible moves for the attacker and make him move
            Graphique.draw_board(Game)
            Possible_moves=Game.available_move_position(rugbyman_attacker)
            Graphique.highlight_move_FElIX(Possible_moves)
            #This function forces the rugbyman to move
            move_rugbyman_after_succesfull_charging(Graphique,rugbyman_attacker,Game.get_ball(),Possible_moves)
            
        else : 
            #If the defender wins the charge
            rugbyman_attacker.set_KO()
            
            #We then have to move the now lost ball to a new position 
            if rugbyman_attacker.get_color()==Color.RED:
                if rugbyman_attacker.get_pos_y()>1:
                    #The first normal position (happens 90% of the time) is just putting the ball behind the attacker
                    Game.get_ball().set_pos([rugbyman_attacker.get_pos_x(),rugbyman_attacker.get_pos_y()-1])
                else:
                    
                    #If the attacker is on the edge of the board we put the ball on the side
                    if rugbyman_attacker.get_pos_x()>1:
                        Game.get_ball().set_pos([rugbyman_attacker.get_pos_x()-1,rugbyman_attacker.get_pos_y()])
                    else:
                        Game.get_ball().set_pos([rugbyman_attacker.get_pos_x()+1,rugbyman_attacker.get_pos_y()])
            else:
                #Same but here the "behind" blue is towards the right 
                if rugbyman_attacker.get_pos_y()<Constants.number_of_columns :
                    Game.get_ball().set_pos([rugbyman_attacker.get_pos_x(),rugbyman_attacker.get_pos_y()-1])
                else:
                    if rugbyman_attacker.get_pos_x()>1:
                        Game.get_ball().set_pos([rugbyman_attacker.get_pos_x()-1,rugbyman_attacker.get_pos_y()])
                    else:
                        Game.get_ball().set_pos([rugbyman_attacker.get_pos_x()+1,rugbyman_attacker.get_pos_y()])
            rugbyman_attacker.set_possesion(False)
            
            #If the rugbyman doing the charging was far from the the defender we have to replace it like he made 
            #the move one square by one square
            if norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>1:
                min_norm=100
                #we iterate over the possible moves of the attacker (moves where he could have been if he took the time to move 
                # his rugbyman one square by one square)
                for move in Possible_moves:
                    
                    #The relocation has to be close to the defender
                    if norm(move[:2],rugbyman_defender.get_pos())==1:
                        #The closest square is the natural choice
                        if norm(move[:2],rugbyman_attacker.get_pos())<min_norm:

                            min_norm=norm([move[0],move[1]],rugbyman_attacker.get_pos())
                            new_attacker_pos=[move[0],move[1]]
                            new_attacker_cost=move[2]
                if min_norm<100:
                    rugbyman_attacker.set_pos(new_attacker_pos)
                    rugbyman_attacker.set_move_left(new_attacker_cost)
        return rugbyman_attacker 
    else:
        print("You don't have enough move points left to charge this rugbyman")
        return False

def tackling(Graphique,Game,rugbyman_attacker, rugbyman_defender,Possible_moves):
    
    print("Players have to choose their cards")
    if Game.is_rugbyman_on_ball()==rugbyman_defender:
        print("Red Player has to choose his card")
        c_red=choose_cards(Graphique,Game.get_player_red())
        print("Blue Player has to choose his card")
        Graphique.draw_board(Game)
        c_blue=choose_cards(Graphique,Game.get_player_blue())

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
                Game.get_ball().set_pos(rugbyman_attacker.get_pos())
            
            if rugbyman_defender.get_color()==Color.RED:
                    if rugbyman_defender.get_pos_y()>0:
                        Game.get_ball().set_pos([rugbyman_defender.get_pos_x(),rugbyman_defender.get_pos_y()-1])
                    else:
                        if rugbyman_defender.get_pos_x()>0:
                            Game.get_ball().set_pos([rugbyman_defender.get_pos_x()-1,rugbyman_defender.get_pos_y()])
                        else:
                            Game.get_ball().set_pos([rugbyman_defender.get_pos_x()+1,rugbyman_defender.get_pos_y()])
            else:
                if rugbyman_defender.get_pos_y()<Constants.number_of_columns :
                    Game.get_ball().set_pos([rugbyman_defender.get_pos_x(),rugbyman_defender.get_pos_y()+1])
                else:
                    if rugbyman_defender.get_pos_x()>0:
                        Game.get_ball().set_pos([rugbyman_defender.get_pos_x()-1,rugbyman_defender.get_pos_y()])
                    else:
                        Game.get_ball().set_pos([rugbyman_defender.get_pos_x()+1,rugbyman_defender.get_pos_y()])
            rugbyman_attacker.set_possesion(False)
        else :
            rugbyman_attacker.set_KO()
            #If the rugbyman doing the tackling was far from the the defender
        if norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>1:
            min_norm=100
            for moves in Possible_moves:
                if norm([moves[0],moves[1]],rugbyman_defender.get_pos())==1:
                    if (norm([moves[0],moves[1]],rugbyman_attacker.get_pos())<min_norm
                        and moves[3]): #moves[3] ensure that the square is free
                     
                        min_norm=norm([moves[0],moves[1]],rugbyman_attacker.get_pos())
                        new_attacker_pos=[moves[0],moves[1]]
                        new_attacker_cost=moves[2]
            if min_norm<100: #why not ???
                rugbyman_attacker.set_pos(new_attacker_pos)
                rugbyman_attacker.set_move_left(new_attacker_cost)

            if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus()+1:
                print("Perfect tackle, the attacker keeps the ball ")
                Game.get_ball().set_pos(new_attacker_pos)
                Game.get_ball().set_carrier(rugbyman_attacker)
                rugbyman_attacker.set_possesion(True)
        else :
            if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus()+1:
                print("Perfect tackle, the attacker keeps the ball ")
                Game.get_ball().set_pos(rugbyman_attacker.get_pos())
                Game.get_ball().set_carrier(rugbyman_attacker)
                rugbyman_attacker.set_possesion(True)

        return rugbyman_attacker 
    else :
        print("You can only tackle the rugbyman with the ball")
        return False

def action_rugbyman(Graphique,rugbyman, Game,Possible_moves, Graphisme):

    pos,cond = Graphisme.get_hitbox_on_click()

    Possible_moves_without_scope_and_bool=[[k[0],k[1]] for k in Possible_moves]

    if pos in Possible_moves_without_scope_and_bool:
        i=Possible_moves_without_scope_and_bool.index(pos)
        if Possible_moves[i][3]:
            return move_rugbyman(pos,rugbyman,Game.get_ball(),Possible_moves[i][2])
        else :
            
            if Game.is_rugbyman_on_ball()==rugbyman:
                return charging(Graphique,Game,rugbyman,Game.which_rugbyman_in_pos(pos),Possible_moves)
            elif Game.get_ball().get_pos()==pos:
                return tackling(Graphique,Game,rugbyman,Game.which_rugbyman_in_pos(pos),Possible_moves) 
            else :
                print("You can only tackle the rugbyman with the ball")  
                return False
    else :
        print("You can't move to this position")
        return False

def available_backward_pass( rugbyman ,Game):
    available = []

    current_x = rugbyman.get_pos_x()
    current_y = rugbyman.get_pos_y()

    pass_scope = Constants.back_pass_scope

    if rugbyman.get_color() is Color.RED:
        for x in range(current_x - pass_scope, current_x + pass_scope+1):
            for y in range( current_y - pass_scope, current_y):
                if Game.is_position_correct(x, y):
                    available.append([x, y])

    if rugbyman.get_color() is Color.BLUE:
        for x in range(current_x - pass_scope, current_x + pass_scope+1):
            for y in range( current_y +1, current_y+pass_scope+1):
                if Game.is_position_correct(x, y):
                    available.append([x, y])

    return available

def available_forward_pass( rugbyman ,Game):
    available = []

    current_x = rugbyman.get_pos_x()
    current_y = rugbyman.get_pos_y()

    pass_scope = Constants.forward_pass_scope

    cond = True
    
    if rugbyman.get_color() is Color.BLUE:
        for rugbyman in Game.get_player_turn().get_rugbymen():
            if rugbyman.get_pos_y()<current_y:
                cond = False

        if cond :
            for x in range(current_x - pass_scope, current_x + pass_scope+1):
                for y in range( current_y - pass_scope, current_y):
                    if Game.is_position_correct(x, y):
                        available.append([x, y])

    if rugbyman.get_color() is Color.RED:
        for rugbyman in Game.get_player_turn().get_rugbymen():
            if rugbyman.get_pos_y()>current_y:
                cond = False
        if cond :
            for x in range(current_x - pass_scope, current_x + pass_scope+1):
                for y in range( current_y +1, current_y+pass_scope+1):
                    if Game.is_position_correct(x, y):
                        available.append([x, y])

    return available

def available_pass( Game):
    rugbyman=Game.is_rugbyman_on_ball()

    return available_forward_pass(rugbyman ,Game)+available_backward_pass(rugbyman ,Game)

def norm(pos1,pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

def make_pass(Game,Graph,Possible_passes):
    pos,cond=front.Graphique.get_hitbox_on_click(Graph)

    if pos in Possible_passes:
        #former_owner is the rugbyman who had the ball before the pass
        former_owner=Game.is_rugbyman_on_ball()

        #If the pass is backward (meaning it can be catched)
        if (former_owner.get_color() is Color.RED
            and pos[1] < former_owner.get_pos_y()):

            #For each rugbyman of the opposing team we have to check if they can catch the ball
            min=100
            for rugbyman in Game.get_player_blue().get_rugbymen():
                #We check if the rugbyman is in the right position to catch the ball
                if (rugbyman.get_pos_y() < former_owner.get_pos_y() 
                    and rugbyman.get_pos_y() >= pos[1]
                    and rugbyman.get_KO()==0):

                    #Receiver and adversary are both above the thrower or both under 
                    #This condition this necessary since the norm alone isnt enough
                    if (rugbyman.get_pos_x() -former_owner.get_pos_x())*(pos[0] -former_owner.get_pos_x())>=0:

                        #We check if the rugbyman is closer to the ball than the former owner
                        if (norm(rugbyman.get_pos(),pos)<norm(former_owner.get_pos(),pos)
                            and min>norm(rugbyman.get_pos(),former_owner.get_pos())):
                            rugbyman_closer=rugbyman
                            min=norm(rugbyman.get_pos(),former_owner.get_pos()) 
            if min<100:
                rugbyman_closer.set_possesion(True)
                former_owner.set_possesion(False)
                Game.get_ball().set_carrier(rugbyman_closer)
                Game.get_ball().set_pos(rugbyman_closer.get_pos())
                return True
                        
        #Same with the blue the only difference is that the receiver has to be above the thrower
        if (former_owner.get_color() is Color.BLUE
            and pos[1] > former_owner.get_pos_y()):
            min=100
            for rugbyman in Game.get_player_red().get_rugbymen():
                if (rugbyman.get_pos_y() > former_owner.get_pos_y() 
                    and rugbyman.get_pos_y() <= pos[1]
                    and rugbyman.get_KO()==0):
                    #ensure there on the same side of the passing position set
                    if (rugbyman.get_pos_x() -former_owner.get_pos_x())*(pos[0] -former_owner.get_pos_x())>=0:
                        
                        if (norm(rugbyman.get_pos(),pos)<norm(former_owner.get_pos(),pos)
                            and min>norm(rugbyman.get_pos(),former_owner.get_pos())):   
                            rugbyman_closer=rugbyman
                            min=norm(rugbyman.get_pos(),former_owner.get_pos())
            if min<100:
                rugbyman_closer.set_possesion(True)
                former_owner.set_possesion(False)
                Game.get_ball().set_carrier(rugbyman_closer)
                Game.get_ball().set_pos(rugbyman_closer.get_pos())
                return True
        
        Game.is_rugbyman_on_ball().set_possesion(False)
        Game.get_ball().set_pos(pos)

        if Game.is_rugbyman_on_ball()!=False:
            Game.is_rugbyman_on_ball().set_possesion(True)

def choose_cards( Graph, player):
        #We draw the cards
        Graph.draw_cards(player)
        #We wait for the player to choose his cards
        
        is_card_returned=True
        active_cards=player.get_deck_int()
        pos,cond=Graph.get_hitbox_on_click()
        while pos==False :
            Graph.draw_cards(player)
            pos,cond=Graph.get_hitbox_on_click()

        if player.get_color()==Color.RED:
            print("Red player Chooses his cards")

            while is_card_returned:
                while pos[1]>=(Constants.number_of_columns+2)//2 or pos[0]<2 or pos[0]>Constants.number_of_rows-1: 
                    print("Please Click on a card")
                    pos,cond=Graph.get_hitbox_on_click()
                    while pos==False :
                        Graph.draw_cards(player)
                        pos,cond=Graph.get_hitbox_on_click()
                if pos[0]<(Constants.number_of_rows+2)//2:
                    card_number=pos[1]//2+1
                else :
                    card_number=pos[1]//2+4
                if card_number in active_cards:
                    player.choose_card(cards.convert_int_to_card(card_number))
                    is_card_returned=False
                else :
                    print("You can't choose this card")
                    pos,cond=Graph.get_hitbox_on_click()

        if player.get_color()==Color.BLUE:
            print("Blue player Chooses his cards")
            while is_card_returned:
                while pos[1]<=(Constants.number_of_columns+2)//2 or pos[0]<2 or pos[0]>Constants.number_of_rows-1: 
                    print("Please Click on a card")
                    pos,cond=Graph.get_hitbox_on_click()
                    while pos==False :
                        Graph.draw_cards(player)
                        pos,cond=Graph.get_hitbox_on_click()
                if pos[0]<(Constants.number_of_rows+2)//2:
                    card_number=(pos[1]+1)//2-3
                else :
                    card_number=(pos[1]+1)//2
                if card_number in active_cards:
                    player.choose_card(cards.convert_int_to_card(card_number))
                    is_card_returned=False
                else :
                    print("You can't choose this card")
                    pos,cond=Graph.get_hitbox_on_click()
                    while pos==False :
                        Graph.draw_cards(player)
                        pos,cond=Graph.get_hitbox_on_click()

        return card_number


### IA Functions ###

def undo_move_rugbyman( former_rugbyman_pos,former_ball_pos,rugbyman,ball,cost):
        if cost==rugbyman.get_move_points():
            return rugbyman
        
        rugbyman.set_pos(former_rugbyman_pos)
        rugbyman.set_move_left(cost)
        
        if former_rugbyman_pos==former_ball_pos:
            ball.set_pos(former_rugbyman_pos)
        else :
            rugbyman.set_possesion(False)


def make_pass_AI(Game,pos):
    #former_owner is the rugbyman who had the ball before the pass
    former_owner=Game.is_rugbyman_on_ball()
    
    #If the pass is backward (meaning it can be catched)
    if (former_owner.get_color() is Color.RED
        and pos[1] < former_owner.get_pos_y()):

        #For each rugbyman of the opposing team we have to check if they can catch the ball
        min=100
        for rugbyman in Game.get_player_blue().get_rugbymen():
            #We check if the rugbyman is in the right position to catch the ball
            if (rugbyman.get_pos_y() < former_owner.get_pos_y() 
                and rugbyman.get_pos_y() >= pos[1]
                and rugbyman.get_KO()==0):

                #Receiver and adversary are both above the thrower or both under 
                #This condition this necessary since the norm alone isnt enough
                if (rugbyman.get_pos_x() -former_owner.get_pos_x())*(pos[0] -former_owner.get_pos_x())>=0:

                    #We check if the rugbyman is closer to the ball than the former owner
                    if (norm(rugbyman.get_pos(),pos)<norm(former_owner.get_pos(),pos)
                        and min>norm(rugbyman.get_pos(),former_owner.get_pos())):
                        return False
    #Same with the blue the only difference is that the receiver has to be above the thrower
    if (former_owner.get_color() is Color.BLUE
        and pos[1] > former_owner.get_pos_y()):
        min=100
        for rugbyman in Game.get_player_red().get_rugbymen():
            if (rugbyman.get_pos_y() > former_owner.get_pos_y() 
                and rugbyman.get_pos_y() <= pos[1]
                and rugbyman.get_KO()==0):
                #ensure there on the same side of the passing position set
                if (rugbyman.get_pos_x() -former_owner.get_pos_x())*(pos[0] -former_owner.get_pos_x())>=0:
                    
                    if (norm(rugbyman.get_pos(),pos)<norm(former_owner.get_pos(),pos)
                        and min>norm(rugbyman.get_pos(),former_owner.get_pos())):   
                            return False
                        
    
    Game.is_rugbyman_on_ball().set_possesion(False)
    Game.get_ball().set_pos(pos)

    if Game.is_rugbyman_on_ball()!=False:
        Game.is_rugbyman_on_ball().set_possesion(True)


def undo_pass_AI(Game,former_ball_pos,former_owner):
    if Game.is_rugbyman_on_ball()!=False:
        Game.is_rugbyman_on_ball().set_possesion(False)
    
    Game.get_ball().set_pos(former_ball_pos)
    former_owner.set_possesion(True)
    Game.get_ball().set_carrier(former_owner)    

def action_rugbyman_AI(Game,rugbyman_attacker,rugbyman_defender,Possible_moves):
    if Game.is_rugbyman_on_ball()==rugbyman_attacker:
        return charging_AI(Game,rugbyman_attacker,rugbyman_defender,Possible_moves)
    elif Game.get_ball().get_pos()==rugbyman_defender.get_pos():
        return tackling_AI(Game,rugbyman_attacker,rugbyman_defender,Possible_moves) 
    return False

def charging_AI(Game,rugbyman_attacker, rugbyman_defender,Possible_moves):
    """
    This charging function is meant to be used by the minimax algorithm it does not do anything
    """
    #the condition is >=1 because once he is on him he has to be able to move
    if rugbyman_attacker.get_moves_left()- norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>=1:
        
        #To simplify the logical choice is always the best card (at small depth)
        #Optimization could be made here by making the AI choose the smallest card enabling him to win the charge
        c_red=max(Game.get_player_red().get_deck_int()) 
        c_blue= max(Game.get_player_blue().get_deck_int())

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
            Game.get_ball().set_pos(rugbyman_defender.get_pos()) #A bit useless here since the ball was already in the defender position
            rugbyman_attacker.set_possesion(True)

            #Rugbyman attacker is on defender position we then actualize his position and move left
            rugbyman_attacker.set_pos(rugbyman_defender.get_pos())
            for move in Possible_moves:
                if move[:2]==rugbyman_defender.get_pos():
                    rugbyman_attacker.set_move_left(move[2])
            
            #Here it is hard to choose the best move as it is outside the minimax evaluation yet we will pick the best move still
            Possible_moves=Game.available_move_position(rugbyman_attacker)
            award=-10000
            for move in Possible_moves:
                rugbyman_attacker.set_pos(move[:2])
                if award<Game.award_function(Game.get_player_turn()):
                    award=Game.award_function(Game.get_player_turn())
                    best_move=move
                rugbyman_attacker.set_pos(rugbyman_defender.get_pos())
            rugbyman_attacker.set_pos(best_move[:2])
            return True 
            
        else : 
            #if the attacker has more chance of losing the battle then it is not worth it
            return False
    else:
        return False
    

def tackling_AI(Game,rugbyman_attacker, rugbyman_defender,Possible_moves,Graphique):

    if Game.is_rugbyman_on_ball()==rugbyman_defender:
        
        c_blue= 1
        c_red=max(Game.get_player_red().get_deck_int())


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
                Game.get_ball().set_pos(rugbyman_attacker.get_pos())
            
            if rugbyman_defender.get_color()==Color.RED:
                    if rugbyman_defender.get_pos_y()>0:
                        Game.get_ball().set_pos([rugbyman_defender.get_pos_x(),rugbyman_defender.get_pos_y()-1])
                    else:
                        if rugbyman_defender.get_pos_x()>0:
                            Game.get_ball().set_pos([rugbyman_defender.get_pos_x()-1,rugbyman_defender.get_pos_y()])
                        else:
                            Game.get_ball().set_pos([rugbyman_defender.get_pos_x()+1,rugbyman_defender.get_pos_y()])
            else:
                if rugbyman_defender.get_pos_y()<Constants.number_of_columns :
                    Game.get_ball().set_pos([rugbyman_defender.get_pos_x(),rugbyman_defender.get_pos_y()+1])
                else:
                    if rugbyman_defender.get_pos_x()>0:
                        Game.get_ball().set_pos([rugbyman_defender.get_pos_x()-1,rugbyman_defender.get_pos_y()])
                    else:
                        Game.get_ball().set_pos([rugbyman_defender.get_pos_x()+1,rugbyman_defender.get_pos_y()])
            rugbyman_attacker.set_possesion(False)
        else :
            return False 
        if norm(rugbyman_attacker.get_pos(),rugbyman_defender.get_pos())>1:
            min_norm=100
            for moves in Possible_moves:
                if norm([moves[0],moves[1]],rugbyman_defender.get_pos())==1:
                    if (norm([moves[0],moves[1]],rugbyman_attacker.get_pos())<min_norm
                        and moves[3]): #moves[3] ensure that the square is free
                     
                        min_norm=norm([moves[0],moves[1]],rugbyman_attacker.get_pos())
                        new_attacker_pos=[moves[0],moves[1]]
                        new_attacker_cost=moves[2]
            if min_norm<100: #why not ???
                rugbyman_attacker.set_pos(new_attacker_pos)
                rugbyman_attacker.set_move_left(new_attacker_cost)

        if c_attacker+rugbyman_attacker.get_attack_bonus()>c_defender+rugbyman_defender.get_defense_bonus()+1:
            Game.get_ball().set_pos(new_attacker_pos)
            Game.get_ball().set_carrier(rugbyman_attacker)
            rugbyman_attacker.set_possesion(True)
        

        return True 
    else :
        return False