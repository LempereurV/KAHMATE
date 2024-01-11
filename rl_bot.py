import actions
import random
import numpy as np


#On pourrait évaluer les positions dans l'ordre de proximité à la balle 
#En mettant une duréé maximale de calcul pour l'IA, on pourrait évaluer le plus de noeuds possibles dans le temps imparti       
def rl_bot(Game,player,env):
    count=0



    possible_moves=Game.every_possible_move(player)
    
    maxeval=-1000
    ball_pos=False


    #L'idée que j'avais était d'évaluer les rugbyman par proximité avec la balle de sorte que l'on puisse réduire le nombre d'opérations 
    #Lorsqu'un personnage à la possibilité de tacler il le fait directement cf vrai rugby dans ce cas il faut que le joueur adverse
    #puisse reprendre la main sur l'action pour choisir sa carte. 
    #Si l'action est réussie on enchaine normalement sinon on réessaye avec un autre joeuur si possible 
    for i_1 in range(len(possible_moves)):
        
        
        actions1=possible_moves[i_1]
        former_pos_rugbyman_1=actions1[0].get_pos()
        moove_points1=actions1[0].get_move_points()
        
        for i_2 in range(i_1+1,len(possible_moves)):
            
            actions2=possible_moves[i_2]
            
            former_pos_rugbyman_2=actions2[0].get_pos()
            moove_points2=actions2[0].get_move_points()

            former_ball_pos=Game.get_ball().get_pos()

            

            for j_1 in range(1,len(actions1)):
                if not actions1[j_1][-1]:
                    print("caca")
                    rugbyman_defender=Game.which_rugbyman_in_pos([actions1[j_1][0],actions1[j_1][1]])
                    print(actions1[0])
                    if actions.action_rugbyman_AI(Game,actions1[0],rugbyman_defender,actions1[1:]):
                        rugbyman_defender.set_KO_0()
                        print("boudin")
                    continue
                    
                    
                
                
                actions.move_rugbyman([actions1[j_1][0],actions1[j_1][1]],actions1[0],Game.get_ball(),actions1[j_1][2])

                #The first rugbyman goes forward then throw the ball
                if actions1[0].has_ball():
                    former_ball_pos=Game.get_ball().get_pos()
                    for possible_throw in actions.available_pass(Game):
                        actions.make_pass_AI(Game,possible_throw)
                
                        for j_2 in range (1,len(actions2)):
                            if not actions2[j_2][-1]:
                                continue
                            actions.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],actions2[0],Game.get_ball(),actions2[j_2][2])
                            #Implementation of the minimax recursive function

                            Max=Game.award_function(player)
                            count+=1
                            if Max>maxeval or (Max==maxeval and random.randint(1,100)>50):
                                maxeval=Max
                                action1=[actions1[0]]+actions1[j_1]
                                action2=[actions2[0]]+actions2[j_2]
                                ball_pos=possible_throw
                            
                            
                            
                            actions.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos,actions2[0],Game.get_ball(),moove_points2)
                        actions.undo_pass_AI(Game,former_ball_pos,actions1[0])
                        

                for j_2 in range(1,len(actions2)):
                    if not actions2[j_2][-1]:
                        continue

                    #Ensure move 2 does not supepose move 1
                    if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                        continue
                    actions.move_rugbyman([actions2[j_2][0],actions2[j_2][1]],actions2[0],Game.get_ball(),actions2[j_2][2])
                    Max=Game.award_function(player)
                    if Max>maxeval or (Max==maxeval and random.randint(1,100)>50):
                        count+=1
                        maxeval=Max
                        action1=[actions1[0]]+actions1[j_1]
                        action2=[actions2[0]]+actions2[j_2]
                        ball_pos=False
                    
                    actions.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos,actions2[0],Game.get_ball(),moove_points2)
                actions.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos,actions1[0],Game.get_ball(),moove_points1)

    print("Nombre de noeuds évalués : ",count)
    return [action1,action2],ball_pos









            
    """
        for i in range (1,len(action)):
            actions.move_rugbyman([action[i][0],action[i][1]],action[0],Game.get_ball(),action[i][2])
            Max=minimax(Game,player,depth-1,action1,action2)
            if Max>maxeval:
                maxeval=Max
                if depth==2:
                    action1=[action[0]]+action[i]
                if depth==1:
                    action2=[action[0]]+action[i]
            actions.move_rugbyman(pos,action[0],Game.get_ball(),moove_points)
    return maxeval
    """
        
    