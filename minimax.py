import game 
import actions
import time 
import random 

#For now the minimax function returns the best move for the player for only one turn (move that maximizes the award)
#The structure of the tree is as follows:
#The first node has 6 children (6 possible rugbymen) 
#His children have maixmum 4 children (4 possible moves)
#His grand children have 5 children (5 remaining rugbymen)
#His great grand children have maximum 4 children (4 possible moves)
#His great great grand children have maximum 4 children (4 possible moves)
#And so on until the maximum move points are reached

#On pourrait évaluer les positions dans l'ordre de proximité à la balle 
#En mettant une duréé maximale de calcul pour l'IA, on pourrait évaluer le plus de noeuds possibles dans le temps imparti       
def minimax(game,player,Graphique):
    count=0


    possible_moves=game.every_possible_move(player)
    
    maxeval=-1000
    ball_pos=False



    for i_1 in range(len(possible_moves)):
        
        actions1=possible_moves[i_1]

        former_pos_rugbyman_1=actions1[0].get_pos()
        moove_points1=actions1[0].get_move_points()
        
        for i_2 in range(i_1+1,len(possible_moves)):
            
            actions2=possible_moves[i_2]
            
            former_pos_rugbyman_2=actions2[0].get_pos()
            moove_points2=actions2[0].get_move_points()

            former_ball_pos=game.get_ball().get_pos()

            

            for j_1 in range(1,len(actions1)):

                if not actions1[j_1][-1]:
                    continue
                    
                    
                
                
                actions.move_rugbyman([actions1[j_1][0],actions1[j_1][1]],actions1[0],game.get_ball(),actions1[j_1][2])

                #The first rugbyman goes forward then throw the ball
                if actions1[0].has_ball():
                    former_ball_pos=game.get_ball().get_pos()
                    for possible_throw in actions.available_pass(game):
                        actions.make_pass_AI(game,possible_throw)
                
                        for j_2 in range (1,len(actions2)):
                            if not actions2[j_2][-1]:
                                continue
                            actions.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],actions2[0],game.get_ball(),actions2[j_2][2])
                            #Implementation of the minimax recursive function

                            Max=game.award_function(player)
                            count+=1
                            if Max>maxeval or (Max==maxeval and random.randint(1,100)>50):
                                maxeval=Max
                                action1=[actions1[0]]+actions1[j_1]
                                action2=[actions2[0]]+actions2[j_2]
                                ball_pos=possible_throw
                            
                            
                            
                            actions.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos,actions2[0],game.get_ball(),moove_points2)
                        actions.undo_pass_AI(game,former_ball_pos,actions1[0])
                        

                for j_2 in range(1,len(actions2)):
                    if not actions2[j_2][-1]:
                        continue

                    #Ensure move 2 does not supepose move 1
                    if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                        continue
                    actions.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],actions2[0],game.get_ball(),actions2[j_2][2])
                    Max=game.award_function(player)
                    if Max>maxeval or (Max==maxeval and random.randint(1,100)>50):
                        count+=1
                        maxeval=Max
                        action1=[actions1[0]]+actions1[j_1]
                        action2=[actions2[0]]+actions2[j_2]
                        ball_pos=False
                    
                    actions.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos,actions2[0],game.get_ball(),moove_points2)
                actions.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos,actions1[0],game.get_ball(),moove_points1)

    print("Nombre de noeuds évalués : ",count)
    return [action1,action2],ball_pos









            
    """
        for i in range (1,len(action)):
            actions.move_rugbyman([action[i][0],action[i][1]],action[0],game.get_ball(),action[i][2])
            Max=minimax(game,player,depth-1,action1,action2)
            if Max>maxeval:
                maxeval=Max
                if depth==2:
                    action1=[action[0]]+action[i]
                if depth==1:
                    action2=[action[0]]+action[i]
            actions.move_rugbyman(pos,action[0],game.get_ball(),moove_points)
    return maxeval
    """
        
    