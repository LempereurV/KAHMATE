import game 
import actions as actions_for_game 
import time 
import random 
from color import Color


def minimax(Game,depth,first_turn,alpha,beta,player,moves,graphique):

    

    if depth==0 :
        return Game.reward_function(player)
    if Game.is_game_over():
        if player.get_color()==Color.RED:
            return -float("inf")
        else :
            return float("inf")
    possible_moves=Game.every_possible_move(player)

    ball_pos=False
    
    if player.get_color()==Color.RED:
        maxeval=-float("inf")

        #L'idée que j'avais était d'évaluer les rugbyman par proximité avec la balle de sorte que l'on puisse réduire le nombre d'opérations 
        #Lorsqu'un personnage à la possibilité de tacler il le fait directement cf vrai rugby dans ce cas il faut que le joueur adverse
        #puisse reprendre la main sur l'action pour choisir sa carte. 
        #Si l'action est réussit on enchaine normalement sinon on réessaye avec un autre joeuur si possible
        
        tries_tackling=False
        former_ball_pos_1=Game.get_ball().get_pos()
        
        for i_1 in range(3):
            
            
            rugbyman1=possible_moves[i_1][0]
            actions1=possible_moves[i_1][1:]
            
            former_pos_rugbyman_1=rugbyman1.get_pos()
            moove_points1=rugbyman1.get_move_points()
            
            for i_2 in range(i_1+1,3):
                
                rugbyman2=possible_moves[i_2][0]
                actions2=possible_moves[i_2][1:]
                
                former_pos_rugbyman_2=rugbyman2.get_pos()
                moove_points2=rugbyman2.get_move_points()


                

                for j_1 in range(len(actions1)):
                    if not actions1[j_1][-1] and first_turn:

                        rugbyman_defender=Game.which_rugbyman_in_pos([actions1[j_1][0],actions1[j_1][1]])
                        
                        #If the defender is in position of tackling he will do it no matter the outcome of the tackle
                        actions_for_game.action_rugbyman_AI(Game,rugbyman1,rugbyman_defender,actions1,graphique)

                        #FROM THERE THE GENERAL FOR LOOP DOES NOT CONTINUE 

                        for i_2_p in range(i_1+1,3):
                
                            rugbyman2=possible_moves[i_2_p][0]
                            actions2=possible_moves[i_2_p][1:]
                            
                            former_pos_rugbyman_2=rugbyman2.get_pos()
                            moove_points2=rugbyman2.get_move_points()

                            for j_2 in range (len(actions2)):
                                if ( not actions2[j_2][-1] and first_turn 
                                    and not actions_for_game.action_rugbyman_AI(Game,rugbyman2,rugbyman_defender,actions1,graphique==False)):

                                    

                                    moves[0]=False
                                    moves[1]=False
                                    moves[2]=None
                                    return 0
                                else :
                                    if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                                        continue
                                    actions_for_game.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],rugbyman2,Game.get_ball(),actions2[j_2][2])

                                    eval=minimax(Game,depth-1,False,alpha,beta,Game.get_player_blue(),moves,graphique)

                                    if eval>maxeval:
                                        maxeval=eval
                                        if first_turn:
                                            moves[0]=[rugbyman1]+actions1[j_1]
                                            moves[1]=[rugbyman2]+actions2[j_2]
                                            moves[2]=None
                                
                                
                                    alpha=max(alpha,maxeval)
                                        
                                        
                                    actions_for_game.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_1,rugbyman2,Game.get_ball(),moove_points2)

                                    if beta<=alpha:
                                        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)
                                        return maxeval
                                    
                    actions_for_game.move_rugbyman([actions1[j_1][0],actions1[j_1][1]],rugbyman1,Game.get_ball(),actions1[j_1][2])

                    #The first rugbyman moves then throw the ball (if he can)
                    if rugbyman1.has_ball():
                        former_ball_pos_2=Game.get_ball().get_pos()


                        for possible_throw in actions_for_game.available_pass(Game):
                            if actions_for_game.make_pass_AI(Game,possible_throw)==False:
                                actions_for_game.undo_pass_AI(Game,former_ball_pos_2,rugbyman1)
                                continue
                            else :  
                                for j_2 in range (len(actions2)):
                                    if not actions2[j_2][-1]:
                                        continue
                                    if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                                        continue
                                    actions_for_game.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],rugbyman2,Game.get_ball(),actions2[j_2][2])
                                    

                                    eval=minimax(Game,depth-1,False,alpha,beta,Game.get_player_blue(),moves,graphique)

                                    if eval>maxeval:
                                        maxeval=eval
                                        if first_turn:
                                            moves[0]=[rugbyman1]+actions1[j_1]
                                            moves[1]=[rugbyman2]+actions2[j_2]
                                            moves[2]=possible_throw
                                    
                                    
                                    alpha=max(alpha,maxeval)

                                    
                                    actions_for_game.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_2,rugbyman2,Game.get_ball(),moove_points2)
                                    if beta<=alpha:
                                        Game.get_ball().set_pos(former_ball_pos_1)
                                        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)
                                        actions_for_game.undo_pass_AI(Game,former_ball_pos_1,rugbyman1)
                                        return maxeval

                                    actions_for_game.undo_pass_AI(Game,former_ball_pos_2,rugbyman1)

                    #Also necessary if rugbyman has ball
                    for j_2 in range(len(actions2)):
                        if not actions2[j_2][-1]:
                            continue

                        #Ensure move 2 does not superpose move 1
                        if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                            continue
                        actions_for_game.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],rugbyman2,Game.get_ball(),actions2[j_2][2])

                        eval=minimax(Game,depth-1,False,alpha,beta,Game.get_player_blue(),moves,graphique)

                        if eval>maxeval:
                            maxeval=eval
                            if first_turn:
                                moves[0]=[rugbyman1]+actions1[j_1]
                                moves[1]=[rugbyman2]+actions2[j_2]
                                moves[2]=None
                                    
                                    
                        alpha=max(alpha,maxeval)
                        
                        
                        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_1,rugbyman2,Game.get_ball(),moove_points2)

                        if beta<=alpha:
                            actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)
                            return maxeval

                    actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)
        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)


        return maxeval


    else:
        mineval=float("inf")

        #L'idée que j'avais était d'évaluer les rugbyman par proximité avec la balle de sorte que l'on puisse réduire le nombre d'opérations 
        #Lorsqu'un personnage à la possibilité de tacler il le fait directement cf vrai rugby dans ce cas il faut que le joueur adverse
        #puisse reprendre la main sur l'action pour choisir sa carte. 
        #Si l'action est réussit on enchaine normalement sinon on réessaye avec un autre joeuur si possible
        
        tries_tackling=False
        former_ball_pos_1=Game.get_ball().get_pos()
        
        for i_1 in range(3):
            
            
            rugbyman1=possible_moves[i_1][0]
            actions1=possible_moves[i_1][1:]
            
            former_pos_rugbyman_1=rugbyman1.get_pos()
            moove_points1=rugbyman1.get_move_points()
            
            for i_2 in range(i_1+1,3):
                
                rugbyman2=possible_moves[i_2][0]
                actions2=possible_moves[i_2][1:]
                
                former_pos_rugbyman_2=rugbyman2.get_pos()
                moove_points2=rugbyman2.get_move_points()


                

                for j_1 in range(len(actions1)):
                    if not actions1[j_1][-1]:
                        """
                        #FROM THERE THE GENERAL FOR LOOP DOES NOT CONTINUE 
                        #Because tackling the adversary is the first priority

                        rugbyman_defender=Game.which_rugbyman_in_pos([actions1[j_1][0],actions1[j_1][1]])
                        
                        #If the defender is in position of tackling he will do it no matter the outcome of the tackle
                        if actions_for_game.action_rugbyman_AI(Game,rugbyman1,rugbyman_defender,actions1,graphique):
                            
                            #
                        else :
                        """
                        continue

                        
                        

                    actions_for_game.move_rugbyman([actions1[j_1][0],actions1[j_1][1]],rugbyman1,Game.get_ball(),actions1[j_1][2])

                    #The first rugbyman moves then throw the ball (if he can)
                    former_ball_pos_2=Game.get_ball().get_pos()
                    if rugbyman1.has_ball():

                        

                        for possible_throw in actions_for_game.available_pass(Game):

                            if actions_for_game.make_pass_AI(Game,possible_throw)==False:
                                actions_for_game.undo_pass_AI(Game,former_ball_pos_2,rugbyman1)
                                continue
                            else :  
                                for j_2 in range (len(actions2)):
                                    if not actions2[j_2][-1]:
                                        continue

                                    if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                                        continue
                                    actions_for_game.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],rugbyman2,Game.get_ball(),actions2[j_2][2])

                                    eval=minimax(Game,depth-1,False,alpha,beta,Game.get_player_red(),moves,graphique)

                                    if eval<mineval:
                                        mineval=eval
                                        if first_turn:
                                            moves[0]=[rugbyman1]+actions1[j_1]
                                            moves[1]=[rugbyman2]+actions2[j_2]
                                            moves[2]=possible_throw
                                    
                                    
                                    beta=min(beta,eval)

                                    
                                    actions_for_game.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_2,rugbyman2,Game.get_ball(),moove_points2)

                                    if beta<=alpha:
                                        actions_for_game.undo_pass_AI(Game,former_ball_pos_1,rugbyman1)
                                        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)
                                        return mineval

                                actions_for_game.undo_pass_AI(Game,former_ball_pos_2,rugbyman1)

                    actions_for_game.undo_pass_AI(Game,former_ball_pos_1,rugbyman1)

                    #Also necessary if rugbyman has ball
                    for j_2 in range(len(actions2)):
                        if not actions2[j_2][-1]:
                            continue

                        #Ensure move 2 does not superpose move 1
                        if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                            continue
                        if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                            continue
                        actions_for_game.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],rugbyman2,Game.get_ball(),actions2[j_2][2])

                        eval=minimax(Game,depth-1,False,alpha,beta,Game.get_player_red(),moves,graphique)

                        if eval<mineval:
                            mineval=eval
                            if first_turn:
                                moves[0]=[rugbyman1]+actions1[j_1]
                                moves[1]=[rugbyman2]+actions2[j_2]
                                moves[2]=None
                                    
                                    
                        beta=min(beta,mineval)
                        
                        
                        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_2,rugbyman2,Game.get_ball(),moove_points2)

                        if beta<=alpha:
                            actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)
                            return mineval

                    actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)
        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)


        return mineval



def minimax_naif(Game,depth,first_turn,alpha,beta,player,moves,graphique):

    

    if depth==0 :
        return Game.reward_function(player)
    if Game.is_game_over():
        if player.get_color()==Color.RED:
            return float("inf")
        else :
            return -float("inf")
    possible_moves=Game.every_possible_move_naif(player)

    ball_pos=False
    
    if player.get_color()==Color.RED:
        maxeval=-float("inf")
        
        tries_tackling=False
        former_ball_pos_1=Game.get_ball().get_pos()
        
        for i_1 in range(3):
            
            
            rugbyman1=possible_moves[i_1][0]
            actions1=possible_moves[i_1][1:]
            
            former_pos_rugbyman_1=rugbyman1.get_pos()
            moove_points1=rugbyman1.get_move_points()
            
            for i_2 in range(i_1+1,3):
                
                rugbyman2=possible_moves[i_2][0]
                actions2=possible_moves[i_2][1:]
                
                former_pos_rugbyman_2=rugbyman2.get_pos()
                moove_points2=rugbyman2.get_move_points()


                

                for j_1 in range(len(actions1)):
                    if not actions1[j_1][-1]:
                        continue

                        
                        

                    actions_for_game.move_rugbyman([actions1[j_1][0],actions1[j_1][1]],rugbyman1,Game.get_ball(),actions1[j_1][2])

                    #The first rugbyman moves then throw the ball (if he can)
                    if rugbyman1.has_ball():
                        former_ball_pos_2=Game.get_ball().get_pos()


                        for possible_throw in actions_for_game.available_pass(Game):
                            if actions_for_game.make_pass_AI(Game,possible_throw)==False:
                                actions_for_game.undo_pass_AI(Game,former_ball_pos_2,rugbyman1)
                                continue
                            else :  
                                for j_2 in range (len(actions2)):
                                    if not actions2[j_2][-1]:
                                        continue
                                    if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                                        continue
                                    actions_for_game.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],rugbyman2,Game.get_ball(),actions2[j_2][2])
                                    

                                    eval=minimax_naif(Game,depth-1,False,alpha,beta,Game.get_player_blue(),moves,graphique)

                                    if eval>maxeval:
                                        maxeval=eval
                                        if first_turn:
                                            moves[0]=[rugbyman1]+actions1[j_1]
                                            moves[1]=[rugbyman2]+actions2[j_2]
                                            moves[2]=possible_throw
                                    
                                    
                                    alpha=max(alpha,maxeval)

                                    
                                    actions_for_game.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_2,rugbyman2,Game.get_ball(),moove_points2)
                                    player.undo_chosen_rugbymen()
                                    
                                    if beta<=alpha:
                                        Game.get_ball().set_pos(former_ball_pos_1)
                                        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)
                                        actions_for_game.undo_pass_AI(Game,former_ball_pos_1,rugbyman1)
                                        return maxeval

                                    actions_for_game.undo_pass_AI(Game,former_ball_pos_2,rugbyman1)

                    #Also necessary if rugbyman has ball
                    for j_2 in range(len(actions2)):
                        if not actions2[j_2][-1]:
                            continue

                        #Ensure move 2 does not superpose move 1
                        if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                            continue
                        actions_for_game.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],rugbyman2,Game.get_ball(),actions2[j_2][2])

                        eval=minimax_naif(Game,depth-1,False,alpha,beta,Game.get_player_blue(),moves,graphique)

                        if eval>maxeval:
                            maxeval=eval
                            if first_turn:
                                moves[0]=[rugbyman1]+actions1[j_1]
                                moves[1]=[rugbyman2]+actions2[j_2]
                                moves[2]=None
                                    
                                    
                        alpha=max(alpha,maxeval)
                        
                        
                        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_1,rugbyman2,Game.get_ball(),moove_points2)

                        if beta<=alpha:
                            actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)
                            return maxeval

                    actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)
        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)


        return maxeval


    else:
        mineval=float("inf")

        #L'idée que j'avais était d'évaluer les rugbyman par proximité avec la balle de sorte que l'on puisse réduire le nombre d'opérations 
        #Lorsqu'un personnage à la possibilité de tacler il le fait directement cf vrai rugby dans ce cas il faut que le joueur adverse
        #puisse reprendre la main sur l'action pour choisir sa carte. 
        #Si l'action est réussit on enchaine normalement sinon on réessaye avec un autre joeuur si possible
        
        tries_tackling=False
        former_ball_pos_1=Game.get_ball().get_pos()
        
        for i_1 in range(3):
            
            
            rugbyman1=possible_moves[i_1][0]
            actions1=possible_moves[i_1][1:]
            
            former_pos_rugbyman_1=rugbyman1.get_pos()
            moove_points1=rugbyman1.get_move_points()
            
            for i_2 in range(i_1+1,3):
                
                rugbyman2=possible_moves[i_2][0]
                actions2=possible_moves[i_2][1:]
                
                former_pos_rugbyman_2=rugbyman2.get_pos()
                moove_points2=rugbyman2.get_move_points()


                

                for j_1 in range(len(actions1)):
                    if not actions1[j_1][-1]:
                        """
                        #FROM THERE THE GENERAL FOR LOOP DOES NOT CONTINUE 
                        #Because tackling the adversary is the first priority

                        rugbyman_defender=Game.which_rugbyman_in_pos([actions1[j_1][0],actions1[j_1][1]])
                        
                        #If the defender is in position of tackling he will do it no matter the outcome of the tackle
                        if actions_for_game.action_rugbyman_AI(Game,rugbyman1,rugbyman_defender,actions1,graphique):
                            
                            #
                        else :
                        """
                        continue

                        
                        

                    actions_for_game.move_rugbyman([actions1[j_1][0],actions1[j_1][1]],rugbyman1,Game.get_ball(),actions1[j_1][2])

                    #The first rugbyman moves then throw the ball (if he can)
                    former_ball_pos_2=Game.get_ball().get_pos()
                    if rugbyman1.has_ball():

                        

                        for possible_throw in actions_for_game.available_pass(Game):

                            if actions_for_game.make_pass_AI(Game,possible_throw)==False:
                                actions_for_game.undo_pass_AI(Game,former_ball_pos_2,rugbyman1)
                                continue
                            else :  
                                for j_2 in range (len(actions2)):
                                    if not actions2[j_2][-1]:
                                        continue

                                    if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                                        continue
                                    actions_for_game.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],rugbyman2,Game.get_ball(),actions2[j_2][2])

                                    eval=minimax_naif(Game,depth-1,False,alpha,beta,Game.get_player_red(),moves,graphique)

                                    if eval<mineval:
                                        mineval=eval
                                        if first_turn:
                                            moves[0]=[rugbyman1]+actions1[j_1]
                                            moves[1]=[rugbyman2]+actions2[j_2]
                                            moves[2]=possible_throw
                                    
                                    
                                    beta=min(beta,eval)

                                    
                                    actions_for_game.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_2,rugbyman2,Game.get_ball(),moove_points2)

                                    if beta<=alpha:
                                        actions_for_game.undo_pass_AI(Game,former_ball_pos_1,rugbyman1)
                                        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)
                                        return mineval

                                actions_for_game.undo_pass_AI(Game,former_ball_pos_2,rugbyman1)

                    actions_for_game.undo_pass_AI(Game,former_ball_pos_1,rugbyman1)

                    #Also necessary if rugbyman has ball
                    for j_2 in range(len(actions2)):
                        if not actions2[j_2][-1]:
                            continue

                        #Ensure move 2 does not superpose move 1
                        if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                            continue
                        if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                            continue
                        actions_for_game.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],rugbyman2,Game.get_ball(),actions2[j_2][2])

                        eval=minimax_naif(Game,depth-1,False,alpha,beta,Game.get_player_red(),moves,graphique)

                        if eval<mineval:
                            mineval=eval
                            if first_turn:
                                moves[0]=[rugbyman1]+actions1[j_1]
                                moves[1]=[rugbyman2]+actions2[j_2]
                                moves[2]=None
                                    
                                    
                        beta=min(beta,mineval)
                        
                        
                        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_2,rugbyman2,Game.get_ball(),moove_points2)

                        if beta<=alpha:
                            actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)
                            return mineval

                    actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)
        actions_for_game.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,Game.get_ball(),moove_points1)


        return mineval