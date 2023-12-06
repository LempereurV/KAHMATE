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
            front.pygame.display.flip()
            Initialisation = False
        
        #Get whowe turn it is to play

        active_player = Game.get_player_turn()

        while active_player.get_can_play():
            #Get the position of the click
            #pos = Graph.get_hitbox_for_back()
            #which_rugbyman_in_pos returns false if there is no rugbyman in the position, and the rugbyman otherwise
            
            rugbyman_or_bool = Game.which_rugbyman_in_pos(Graph)

            if (rugbyman_or_bool in active_player.get_rugbymen()):
                
                Graph.draw_board(Game)

                possible_move = Game.available_move_position(rugbyman_or_bool)
                Graph.highlight_move_FElIX( possible_move)
                

                #If the player hasnt chosen his two rugbyman yet
                if active_player.get_n_rugbymen()<2:
                    
                    #move_rugbyman returns false if the move is not possible, and the rugbyman otherwise
                    #Note that the move is made in the function
                    rugbyman_or_bool=actions.move_rugbyman(rugbyman_or_bool,possible_move,Graph)

                    #We add the rugbyman to the list of chosen rugbyman if the move is made
                    if rugbyman_or_bool !=False :
                        active_player.add_choosen_rugbymen(rugbyman_or_bool)
                
                #If the rugbyman selected is already in the list of chosen rugbyman, then he can move him
                elif rugbyman_or_bool in active_player.get_chosen_rugbymen() :
                    
                    rugbyman_or_bool=actions.move_rugbyman(rugbyman_or_bool,possible_move,Graph)
                
                active_player.actualize_can_play()
                Graph.draw_board(Game)
                active_player.actualize_can_play()

        ### Partie reset quand les deux joueurs ont joué ###
        Game.refresh_players_rugbymen_stats()
        Game.change_player_turn()




        if event.type == front.pygame.QUIT:
            front.pygame.quit()
            front.sys.exit()
            Game_ON = False
print("Fin du jeu")
