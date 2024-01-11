import game 
import actions as actions_for_game 
import time 
import random 
from color import Color

from timeout_decorator import timeout



@timeout(10)   
def minimax(Game,depth,first_turn,alpha,beta,player,moves,Graphique):

    

    if depth==0 or Game.is_game_over():
        return Game.award_function(player)
    
    possible_moves=Game.every_possible_move(player)

    ball_pos=False
    
    if player.get_color()==Color.RED:
        maxeval=-float("inf")

        #L'idée que j'avais était d'évaluer les rugbyman par proximité avec la balle de sorte que l'on puisse réduire le nombre d'opérations 
        #Lorsqu'un personnage à la possibilité de tacler il le fait directement cf vrai rugby dans ce cas il faut que le joueur adverse
        #puisse reprendre la main sur l'action pour choisir sa carte. 
        #Si l'action est réussit on enchaine normalement sinon on réessaye avec un autre joeuur si possible
        
        tries_tackling=False
        
        for i_1 in range(3):#(len(possible_moves)):
            
            
            rugbyman1=possible_moves[i_1][0]
            actions1=possible_moves[i_1][1:]
            
            former_pos_rugbyman_1=rugbyman1.get_pos()
            moove_points1=rugbyman1.get_move_points()
            
            for i_2 in range(i_1+1,3):#i_1+1,len(possible_moves)):
                
                rugbyman2=possible_moves[i_2][0]
                actions2=possible_moves[i_2][1:]
                
                former_pos_rugbyman_2=rugbyman2.get_pos()
                moove_points2=rugbyman2.get_move_points()

                former_ball_pos=Game.get_ball().get_pos()

                

                for j_1 in range(len(actions1)):
                    if not actions1[j_1][-1]:
                        """
                        #FROM THERE THE GENERAL FOR LOOP DOES NOT CONTINUE 
                        #Because tackling the adversary is the first priority

                        rugbyman_defender=Game.which_rugbyman_in_pos([actions1[j_1][0],actions1[j_1][1]])
                        
                        #If the defender is in position of tackling he will do it no matter the outcome of the tackle
                        if actions_for_game.action_rugbyman_AI(Game,rugbyman1,rugbyman_defender,actions1,Graphique):
                            
                            #
                        else :
                        """
                        continue

                        
                        

                    actions_for_game.move_rugbyman([actions1[j_1][0],actions1[j_1][1]],rugbyman1,Game.get_ball(),actions1[j_1][2])

                    #The first rugbyman moves then throw the ball (if he can)

                    if rugbyman1.has_ball():
                        
                        former_ball_pos=Game.get_ball().get_pos()

                        for possible_throw in actions_for_game.available_pass(Game):

                            if actions_for_game.make_pass_AI(Game,possible_throw)==False:
                                actions_for_game.undo_pass_AI(Game,former_ball_pos,rugbyman1)
                                continue
                            else :  
                                for j_2 in range (len(actions2)):
                                    if not actions2[j_2][-1]:
                                        continue
                                    actions_for_game.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],rugbyman2,Game.get_ball(),actions2[j_2][2])

                                    eval=minimax(Game,depth-1,False,alpha,beta,Game.get_player_blue(),moves,Graphique)

                                    if eval>maxeval:
                                        maxeval=eval
                                        if first_turn:
                                            moves[0]=[rugbyman1]+actions1[j_1]
                                            moves[1]=[rugbyman2]+actions2[j_2]
                                    
                                    
                                    alpha=max(alpha,maxeval)

                                    
                                    actions_for_game.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos,rugbyman2,Game.get_ball(),moove_points2)

                                    if beta<=alpha:
                                        actions_for_game.undo_pass_AI(Game,former_ball_pos,rugbyman1)
                                        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos,rugbyman1,Game.get_ball(),moove_points1)
                                        return maxeval

                                actions_for_game.undo_pass_AI(Game,former_ball_pos,rugbyman1)
                            
                    #Also necessary if rugbyman has ball
                    for j_2 in range(len(actions2)):
                        if not actions2[j_2][-1]:
                            continue

                        #Ensure move 2 does not superpose move 1
                        if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                            continue
                        actions_for_game.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],rugbyman2,Game.get_ball(),actions2[j_2][2])

                        eval=minimax(Game,depth-1,False,alpha,beta,Game.get_player_blue(),moves,Graphique)

                        if eval>maxeval:
                            maxeval=eval
                            if first_turn:
                                moves[0]=[rugbyman1]+actions1[j_1]
                                moves[1]=[rugbyman2]+actions2[j_2]
                                    
                                    
                        alpha=max(alpha,maxeval)
                        
                        
                        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos,rugbyman2,Game.get_ball(),moove_points2)

                        if beta<=alpha:
                            actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos,rugbyman1,Game.get_ball(),moove_points1)
                            return maxeval

                    actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos,rugbyman1,Game.get_ball(),moove_points1)


        return maxeval


    else:
        
        mineval=float("inf")
        tries_tackling=False
        
        for i_1 in range(3):#len(possible_moves)):

            rugbyman1=possible_moves[i_1][0]
            actions1=possible_moves[i_1][1:]
            
            former_pos_rugbyman_1=rugbyman1.get_pos()
            moove_points1=rugbyman1.get_move_points()
            
            for i_2 in range(i_1+1,3):#len(possible_moves)):
                
                rugbyman2=possible_moves[i_2][0]
                actions2=possible_moves[i_2][1:]
                
                former_pos_rugbyman_2=rugbyman2.get_pos()
                moove_points2=rugbyman2.get_move_points()

                former_ball_pos=Game.get_ball().get_pos()

                

                for j_1 in range(len(actions1)):
                    if not actions1[j_1][-1]:
                        """
                        #FROM THERE THE GENERAL FOR LOOP DOES NOT CONTINUE 
                        #Because tackling the adversary is the first priority

                        rugbyman_defender=Game.which_rugbyman_in_pos([actions1[j_1][0],actions1[j_1][1]])
                        
                        #If the defender is in position of tackling he will do it no matter the outcome of the tackle
                        if actions.action_rugbyman_AI(Game,rugbyman1,rugbyman_defender,actions1,Graphique):
                            print("Tackle")
                        """
                        continue

                        
                        

                    actions_for_game.move_rugbyman([actions1[j_1][0],actions1[j_1][1]],rugbyman1,Game.get_ball(),actions1[j_1][2])

                    #The first rugbyman moves then throw the ball (if he can)

                    if rugbyman1.has_ball():
                        
                        former_ball_pos=Game.get_ball().get_pos()

                        for possible_throw in actions_for_game.available_pass(Game):

                            if actions_for_game.make_pass_AI(Game,possible_throw)==False:
                                actions_for_game.undo_pass_AI(Game,former_ball_pos,rugbyman1)
                                continue
                            else :  
                                for j_2 in range (len(actions2)):
                                    if not actions2[j_2][-1]:
                                        continue
                                    actions_for_game.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],rugbyman2,Game.get_ball(),actions2[j_2][2])
                                    #Implementation of the minimax recursive function

                                    eval=minimax(Game,depth-1,False,alpha,beta,Game.get_player_red(),moves,Graphique)

                                    if eval<mineval:
                                        mineval=eval
                                        if first_turn:
                                            moves[0]=[rugbyman1]+actions1[j_1]
                                            moves[1]=[rugbyman2]+actions2[j_2]
                                    
                                    
                                    beta=min(beta,eval)

                                    
                                    actions_for_game.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos,rugbyman2,Game.get_ball(),moove_points2)

                                    if beta<=alpha:
                                        actions_for_game.undo_pass_AI(Game,former_ball_pos,rugbyman1)
                                        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos,rugbyman1,Game.get_ball(),moove_points1)
                                        return mineval

                                actions_for_game.undo_pass_AI(Game,former_ball_pos,rugbyman1)
                            

                    for j_2 in range(len(actions2)):
                        if not actions2[j_2][-1]:
                            continue

                        #Ensure move 2 does not supepose move 1
                        if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                            continue
                        actions_for_game.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],rugbyman2,Game.get_ball(),actions2[j_2][2])

                        eval=minimax(Game,depth-1,False,alpha,beta,Game.get_player_red(),moves,Graphique)

                        if eval<mineval:
                            mineval=eval
                            if first_turn:
                                moves[0]=[rugbyman1]+actions1[j_1]
                                moves[1]=[rugbyman2]+actions2[j_2]
                                    
                                    
                        beta=min(beta,eval)
                        
                        
                        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos,rugbyman2,Game.get_ball(),moove_points2)

                        if beta<=alpha:
                            actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos,rugbyman1,Game.get_ball(),moove_points1)
                            return mineval

                    actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos,rugbyman1,Game.get_ball(),moove_points1)

    return mineval

    

"""

def minimax(Game,depth,first_turn,alpha,beta,player,moves,Graphique):

    possible_moves=Game.every_possible_move(player)

    if depth==0 or Game.is_game_over():
        return Game.award_function(player)
    
    if player.get_color()==Color.RED:

        first_turn+=1
        maxeval=-float("inf")
        former_ball_pos=Game.get_ball().get_pos()

        for move1 in range(len(possible_moves)):

            #rugbyman1=possible_moves[move1][0]
            #actions_rugbyman1=possible_moves[move1][1:]
            
            former_pos_rugbyman1=possible_moves[move1][0].get_pos()
            move_points=possible_moves[move1][0].get_move_points()

            for move2 in range(move1+1,len(possible_moves)):

                #rugbyman2=possible_moves[move2][0]
                #actions_rugbyman2=possible_moves[move2][1:]

                former_pos_rugbyman2=possible_moves[move2][0].get_pos()
                move_points=possible_moves[move2][0].get_move_points()

                for action1 in range(1,len(possible_moves[move1])):
                    if not action1[-1]:
                        continue
                    actions_for_game.move_rugbyman([action1[0],action1[1]],possible_moves[move1][0],Game.get_ball(),action1[2])

                    for action2 in range(1,len(possible_moves[move2])):
                        if not action2[-1]:
                            continue
                        actions_for_game.move_rugbyman([action2[0],action2[1]],possible_moves[move2][0],Game.get_ball(),action2[2])

                        if first_turn%4>2:
                            player=Game.other_player(player)

                        eval=minimax(Game,depth-1,False,alpha,beta,player,moves,Graphique)

                        if eval>maxeval:
                            maxeval=eval
                            moves[1]=[possible_moves[move1][0]]+action1

                        actions_for_game.undo_move_rugbyman(former_pos_rugbyman,former_ball_pos,possible_moves[move2][0],Game.get_ball(),move_points)
                    
                    actions_for_game.undo_move_rugbyman(former_pos_rugbyman,former_ball_pos,possible_moves[move1][0],Game.get_ball(),move_points)

                alpha=max(alpha,maxeval)

                if beta<=alpha:
                    break
            for action in actions_rugbyman1:
                if not action[-1]:
                    continue
                
                actions_for_game.move_rugbyman([action[0],action[1]],rugbyman,Game.get_ball(),action[2])

                
                #Because each player has two turns 
                if first_turn%4>2:
                    player=Game.other_player(player)

                eval=minimax(Game,depth-1,False,alpha,beta,player,moves,Graphique)
                
                if eval>maxeval:
                    maxeval=eval
                    if first_turn<=2:
                        moves[first_turn-1]=[rugbyman]+action
                
                actions_for_game.undo_move_rugbyman(former_pos_rugbyman,former_ball_pos,rugbyman,Game.get_ball(),move_points)


                alpha=max(alpha,maxeval)

                if beta<=alpha:
                    break
        return maxeval
    
    else:
        first_turn+=1
        mineval=float("inf")

        for move in Game.every_possible_move(player):
            i+=1
            if i>3:
                break
            rugbyman=move[0]
            actions_rugbyman=move[1:]

            former_pos_rugbyman=rugbyman.get_pos()
            move_points=rugbyman.get_move_points()
            former_ball_pos=Game.get_ball().get_pos()

            for action in actions_rugbyman: 
                if not action[-1]:
                    continue

                actions_for_game.move_rugbyman([action[0],action[1]],rugbyman,Game.get_ball(),action[2])

                if first_turn<=2:
                    player=Game.other_player(player)

                eval = minimax( Game,depth-1,first_turn,alpha,beta,player,moves,Graphique)

                if eval<mineval:
                    mineval=eval
                    if first_turn<=2:
                        moves[first_turn-1]=[rugbyman]+action

                actions_for_game.undo_move_rugbyman(former_pos_rugbyman,former_ball_pos,rugbyman,Game.get_ball(),move_points)

                beta=min(beta,mineval)

                if beta<=alpha:
                    break
        return mineval
"""