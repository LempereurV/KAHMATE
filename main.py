import front
import players
from color import Color
import rugbymen
import game
import actions 

Initialisation = True
Game_ON = True

while Game_ON:
    for event in front.pygame.event.get():
        ### Partie Initialisation ###
        if Initialisation:
            Graph = front.Graphique()
            Game=game.Game(Graph)
            Graph.display_ball(Game.get_ball())
            front.pygame.display.flip()
            Initialisation = False
            
        
        #Get whowe turn it is to play

        active_player = Game.get_player_turn()

        while active_player.get_can_play():
            #Get the position of the click

            
            #which_rugbyman_in_pos returns false if there is no rugbyman in the position, and the rugbyman otherwise

            
            #Graph.draw_new_hitboxes()
            #rugbyman_or_ball_or_bool = Game.which_rugbyman_in_pos(Graph)
            rugbyman_or_ball_or_bool=Game.what_is_in_pos(Graph)

            if (rugbyman_or_ball_or_bool in active_player.get_rugbymen()):
                
                

                Graph.draw_board(Game)

                possible_move = Game.available_move_position(rugbyman_or_ball_or_bool)
                
                """
                ### A changer
                if active_player.has_ball():
                    pos=Graph.get_hitbox_for_back()
                    if pos in 
                ####
                """
                 #If the rugbyman selected is already in the list of chosen rugbyman, then he can move him
                if rugbyman_or_ball_or_bool in active_player.get_chosen_rugbymen() :
                    Graph.highlight_move_FElIX( possible_move)
                    rugbyman_or_ball_or_bool=actions.move_rugbyman(Game.get_ball(),rugbyman_or_ball_or_bool,possible_move,Graph)
                
                #If the player hasnt chosen his two rugbyman yet
                elif active_player.get_n_rugbymen()<2:
                    Graph.highlight_move_FElIX( possible_move)
                    
                    #move_rugbyman returns false if the move is not possible, and the rugbyman otherwise
                    #Note that the move is made in the function
                    rugbyman_or_ball_or_bool=actions.move_rugbyman(Game.get_ball(),rugbyman_or_ball_or_bool,possible_move,Graph)

                    #We add the rugbyman to the list of chosen rugbyman if the move is made
                    if rugbyman_or_ball_or_bool !=False :
                        active_player.add_choosen_rugbymen(rugbyman_or_ball_or_bool)
                
               
                
                if Game.is_rugbyman_on_ball()!=False :
                    rugbyman_with_ball=Game.is_rugbyman_on_ball()



                active_player.actualize_can_play()
                Graph.draw_board(Game)
                active_player.actualize_can_play()

            elif (rugbyman_or_ball_or_bool ==Game.get_ball()):
                available_pass=actions.available_pass(Game)
                Graph.highlight_move_FElIX( available_pass)
                actions.make_pass(Game,Graph,available_pass)
                Graph.draw_board(Game)
                



        ### Partie reset quand le joueur a fini de jouer  ###
        Game.refresh_players_rugbymen_stats()
        Game.change_player_turn()




        if event.type == front.pygame.QUIT:
            front.pygame.quit()
            front.sys.exit()
            Game_ON = False
print("Fin du jeu")
