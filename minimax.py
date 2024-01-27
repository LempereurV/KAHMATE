from color import Color

class Minimax :
    def __init__(self,game,player,actions,actions_minimax,graphic,depth=2) :
        self.game=game
        self.graphic=graphic
        self.player=player
        self.depth=depth
        self.actions=actions
        self.actions_minimax=actions_minimax

    

    def get_depth(self):
        return self.depth
    
   

                    
                    
    def minimax_red_player(self,depth,alpha,beta,moves,possible_moves):
        maxeval=-float("inf")
            
        tries_tackling=False
        former_ball_pos_1=self.game.get_ball().get_pos()
        
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
                    if not actions1[j_1][-1] and depth==self.depth :
                    
                        rugbyman_defender=self.game.which_rugbyman_in_pos([actions1[j_1][0],actions1[j_1][1]])
                        
                        #If the defender is in position of tackling he will do it no matter the outcome of the tackle
                        self.actions_minimax.action_rugbyman_AI(rugbyman1,rugbyman_defender,actions1)

                        #FROM THERE THE GENERAL FOR LOOP DOES NOT CONTINUE 

                        for i_2_p in range(i_1+1,3):
                
                            rugbyman2=possible_moves[i_2_p][0]
                            actions2=possible_moves[i_2_p][1:]
                            
                            former_pos_rugbyman_2=rugbyman2.get_pos()
                            moove_points2=rugbyman2.get_move_points()

                            for j_2 in range (len(actions2)):
                                if ( not actions2[j_2][-1] and depth==self.depth  
                                    and not self.actions_minimax.action_rugbyman_AI(rugbyman2,rugbyman_defender,actions2)):

                                    

                                    moves[0]=False
                                    moves[1]=False
                                    moves[2]=None
                                    return 0
                                else :
                                    if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                                        continue
                                    self.actions.move_rugbyman(actions2[j_2][:2],rugbyman2,actions2[j_2][2])

                                    eval=self.minimax(depth-1,alpha,beta,moves)

                                    if eval>maxeval:
                                        maxeval=eval
                                        if depth==self.depth :
                                            moves[0]=[rugbyman1]+actions1[j_1]
                                            moves[1]=[rugbyman2]+actions2[j_2]
                                            moves[2]=None
                                
                                
                                    alpha=max(alpha,maxeval)
                                        
                                        
                                    self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_1,rugbyman2,moove_points2)

                                    if beta<=alpha:
                                        self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,moove_points1)
                                        return maxeval
                                    
                    self.actions.move_rugbyman(actions1[j_1][0:2],rugbyman1,actions1[j_1][2])

                    #The first rugbyman moves then throw the ball (if he can)
                    if rugbyman1.has_ball():
                        former_ball_pos_2=self.game.get_ball().get_pos()


                        for possible_throw in self.actions.available_pass():
                            if self.actions_minimax.make_pass_AI(possible_throw)==False:
                                self.actions_minimax.undo_pass_AI(former_ball_pos_2,rugbyman1)
                                continue
                            else :  
                                for j_2 in range (len(actions2)):
                                    if not actions2[j_2][-1]:
                                        continue

                                    #Ensure move 2 does not superpose move 1
                                    if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                                        continue

                                    self.actions.move_rugbyman(actions2[j_2][0:2],rugbyman2,actions2[j_2][2])
                                    

                                    eval=self.minimax(depth-1,alpha,beta,moves)

                                    if eval>maxeval:
                                        maxeval=eval
                                        if depth==self.depth :
                                            moves[0]=[rugbyman1]+actions1[j_1]
                                            moves[1]=[rugbyman2]+actions2[j_2]
                                            moves[2]=possible_throw
                                    
                                    
                                    alpha=max(alpha,maxeval)

                                    
                                    self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_2,rugbyman2,moove_points2)

                                    if beta<=alpha:
                                        self.game.get_ball().set_pos(former_ball_pos_1)
                                        self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,moove_points1)
                                        self.actions_minimax.undo_pass_AI(former_ball_pos_1,rugbyman1)
                                        return maxeval

                                    self.actions_minimax.undo_pass_AI(former_ball_pos_2,rugbyman1)

                    #Also necessary if rugbyman has ball
                    for j_2 in range(len(actions2)):
                        if not actions2[j_2][-1]:
                            continue

                        #Ensure move 2 does not superpose move 1
                        if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                            continue
                        self.actions.move_rugbyman(actions2[j_2][0:2],rugbyman2,actions2[j_2][2])

                        eval=self.minimax(depth-1,alpha,beta,moves)

                        if eval>maxeval:
                            maxeval=eval
                            if depth==self.depth :
                                moves[0]=[rugbyman1]+actions1[j_1]
                                moves[1]=[rugbyman2]+actions2[j_2]
                                moves[2]=None
                                    
                                    
                        alpha=max(alpha,maxeval)
                        
                        
                        self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_1,rugbyman2,moove_points2)

                        if beta<=alpha:
                            self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,moove_points1)
                            return maxeval

                    self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,moove_points1)
        self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,moove_points1)


        return maxeval

    def minimax_blue_player(self,depth,alpha,beta,moves,possible_moves):
        mineval=float("inf")
            
        tries_tackling=False
        former_ball_pos_1=self.game.get_ball().get_pos()
        
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
                    if not actions1[j_1][-1] and depth==self.depth :

                        rugbyman_defender=self.game.which_rugbyman_in_pos([actions1[j_1][0],actions1[j_1][1]])
                        
                        #If the defender is in position of tackling he will do it no matter the outcome of the tackle
                        self.actions_minimax.action_rugbyman_AI(rugbyman1,rugbyman_defender,actions1)

                        #FROM THERE THE GENERAL FOR LOOP DOES NOT CONTINUE 

                        for i_2_p in range(i_1+1,3):
                
                            rugbyman2=possible_moves[i_2_p][0]
                            actions2=possible_moves[i_2_p][1:]
                            
                            former_pos_rugbyman_2=rugbyman2.get_pos()
                            moove_points2=rugbyman2.get_move_points()

                            for j_2 in range (len(actions2)):
                                if ( not actions2[j_2][-1] and depth==self.depth  
                                    and not self.actions_minimax.action_rugbyman_AI(rugbyman2,rugbyman_defender,actions1)):

                                    

                                    moves[0]=False
                                    moves[1]=False
                                    moves[2]=None
                                    return 0
                                else :
                                    if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                                        continue
                                    self.actions.move_rugbyman(actions2[j_2][:2],rugbyman2,actions2[j_2][2])

                                    eval=self.minimax(depth-1,alpha,beta,moves)

                                    if eval<mineval:
                                        mineval=eval
                                        if depth==self.depth :
                                            moves[0]=[rugbyman1]+actions1[j_1]
                                            moves[1]=[rugbyman2]+actions2[j_2]
                                            moves[2]=None
                                
                                
                                    beta=min(beta,mineval)
                                        
                                        
                                    self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_1,rugbyman2,moove_points2)

                                    if beta<=alpha:
                                        self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,moove_points1)
                                        return mineval
                                    
                    self.actions.move_rugbyman(actions1[j_1][0:2],rugbyman1,actions1[j_1][2])

                    #The first rugbyman moves then throw the ball (if he can)
                    if rugbyman1.has_ball():
                        former_ball_pos_2=self.game.get_ball().get_pos()


                        for possible_throw in self.actions.available_pass():
                            if self.actions_minimax.make_pass_AI(possible_throw)==False:
                                self.actions_minimax.undo_pass_AI(former_ball_pos_2,rugbyman1)
                                continue
                            else :  
                                for j_2 in range (len(actions2)):
                                    if not actions2[j_2][-1]:
                                        continue

                                    #Ensure move 2 does not superpose move 1
                                    if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                                        continue

                                    self.actions.move_rugbyman(actions2[j_2][0:2],rugbyman2,actions2[j_2][2])
                                    

                                    eval=self.minimax(depth-1,alpha,beta,moves)

                                    if eval<mineval:
                                        mineval=eval
                                        if depth==self.depth :
                                            moves[0]=[rugbyman1]+actions1[j_1]
                                            moves[1]=[rugbyman2]+actions2[j_2]
                                            moves[2]=possible_throw
                                    
                                    
                                    beta=min(beta,mineval)

                                    
                                    self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_2,rugbyman2,moove_points2)

                                    if beta<=alpha:
                                        self.game.get_ball().set_pos(former_ball_pos_1)
                                        self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,moove_points1)
                                        self.actions_minimax.undo_pass_AI(former_ball_pos_1,rugbyman1)
                                        return mineval

                                    self.actions_minimax.undo_pass_AI(former_ball_pos_2,rugbyman1)

                    #Also necessary if rugbyman has ball
                    for j_2 in range(len(actions2)):
                        if not actions2[j_2][-1]:
                            continue

                        #Ensure move 2 does not superpose move 1
                        if [actions1[j_1][0],actions1[j_1][1]]==[actions2[j_2][0],actions2[j_2][1]]:
                            continue
                        self.actions.move_rugbyman(actions2[j_2][0:2],rugbyman2,actions2[j_2][2])

                        eval=self.minimax(depth-1,alpha,beta,moves)

                        if eval<mineval:
                            mineval=eval
                            if depth==self.depth :
                                moves[0]=[rugbyman1]+actions1[j_1]
                                moves[1]=[rugbyman2]+actions2[j_2]
                                moves[2]=None
                                    
                                    
                        beta=min(beta,mineval)
                        
                        
                        self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_2,former_ball_pos_1,rugbyman2,moove_points2)

                        if beta<=alpha:
                            self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,moove_points1)
                            return mineval

                    self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,moove_points1)
        self.actions_minimax.undo_move_rugbyman(former_pos_rugbyman_1,former_ball_pos_1,rugbyman1,moove_points1)


        return mineval
    
    def minimax(self,depth,alpha,beta,moves):
        
        #We make the action of the corresponding player
        if (self.depth-depth)%2 :
            player=self.game.other_player(self.player)
        else :
            player=self.player
            

        #If the game is over then no need to go further
        if self.game.is_game_over():
            if player.get_color()==Color.RED:
                return -float("inf")
            else :
                return float("inf") 
            
        #If the max depth is reached then we evaluate the board
        if depth==0 :
            return self.game.reward_function(player)
        
        #We get all the possible moves for the player
        possible_moves=self.game.every_possible_move(player)

        ball_pos=False

        if depth==0 :
            return self.game.reward_function(player)
        if self.game.is_game_over():
            if player.get_color()==Color.RED:
                return -float("inf")
            else :
                return float("inf")
        possible_moves=self.game.every_possible_move(player)

        ball_pos=False
        
        if player.get_color()==Color.RED:
            return self.minimax_red_player(depth,alpha,beta,moves,possible_moves)

        else:
            return self.minimax_blue_player(depth,alpha,beta,moves,possible_moves)
            

        