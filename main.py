import front
import players
from color import Color
import rugbymen
import game
import actions 
<<<<<<< HEAD



=======
import minimax
import time
import cProfile
import matplotlib.pyplot as plt
import pstats
>>>>>>> branche_minimax_avant_merge
### Initializations ###
from io import StringIO

<<<<<<< HEAD
=======
import pandas as pd


>>>>>>> branche_minimax_avant_merge
#The Graph 
Graph = front.Graphique()
Game=game.Game(Graph)
Graph.display_ball(Game.get_ball())
front.pygame.display.flip()
Initialisation = False

#Outils de profiling python : profiler 


#This the main loop of the game, the function is_game_over of game is verifying each turn if one rugbyman is in the adversary camp


<<<<<<< HEAD
=======
AI=False    

>>>>>>> branche_minimax_avant_merge
while not Game.is_game_over():
    #We record the time it takes

    active_player = Game.get_player_turn()

 
    if AI and active_player.get_color()==Color.RED:
            ### Partie IA####
            moves=[None,None,None]
            begin=time.time()
            try :
                profiler = cProfile.Profile()
                profiler.enable()

                minimax.minimax(Game,2,True,-float("inf"),float("inf"),Game.get_player_turn(),moves,Graph)
                profiler.disable()


                profiler.disable()

                # Save stats to a string
                stats_stream = StringIO()
                stats = pstats.Stats(profiler, stream=stats_stream)
                stats.sort_stats('cumulative')
                stats.print_stats()





                # Print the raw content of the profiling statistics
                print(stats_stream.getvalue())
                

            except TimeoutError:
                print("Temps trop long")
            end=time.time()
            print("Temps de calcul de l'IA : ",end-begin)

            Graph.draw_board(Game)
            
            if moves[2]!=None:
                Game.get_ball().set_pos(moves[2])
            
            for move in moves[:2]:
                if move!=False:
                    actions.move_rugbyman([move[1],move[2]],move[0],Game.get_ball(),move[3])
            Graph.draw_board(Game)
            active_player.set_can_play(False)
            Game.refresh_players_rugbymen_stats()
            Game.change_player_turn()
            continue


            ### ####

    
    while active_player.get_can_play():
        
        
        Graph.draw_board(Game)

        
        rugbyman_or_ball_or_bool=Game.what_is_in_pos(Graph)

        if (rugbyman_or_ball_or_bool in active_player.get_rugbymen()):

            possible_move = Game.available_move_position(rugbyman_or_ball_or_bool)

            if rugbyman_or_ball_or_bool in active_player.get_chosen_rugbymen() :
                
                Graph.highlight_move_FElIX( possible_move)
                rugbyman_or_ball_or_bool=actions.action_rugbyman(Graph,rugbyman_or_ball_or_bool,
                                                                    Game,
                                                                    possible_move,
                                                                    Graph)
            
            #If the player hasnt chosen his two rugbyman yet
            elif active_player.get_n_rugbymen()<2:
                Graph.highlight_move_FElIX( possible_move)
                
                #move_rugbyman returns false if the move is not possible, and the rugbyman otherwise
                #Note that the move itself is made in the function
                rugbyman_or_ball_or_bool=actions.action_rugbyman(Graph,rugbyman_or_ball_or_bool,
                                                                    Game,
                                                                    possible_move,
                                                                    Graph)
                

                #We add the rugbyman to the list of chosen rugbyman if the move is made
                if rugbyman_or_ball_or_bool !=False :
                    active_player.add_choosen_rugbymen(rugbyman_or_ball_or_bool)

        elif (rugbyman_or_ball_or_bool ==Game.get_ball()):
            available_pass=actions.available_pass(Game)
            if len(available_pass)>0:
                Graph.highlight_pass( available_pass)
                actions.make_pass(Game,Graph,available_pass)

        elif (rugbyman_or_ball_or_bool == True):
            #If the player has resized the screen
            break

        Game.is_rugbyman_on_ball()
        active_player.actualize_can_play()
        Graph.draw_board(Game)
        #Redraw cards does not suffice

        

    ### Partie reset quand le joueur a fini de jouer  ###
    Game.refresh_players_rugbymen_stats()
    Game.change_player_turn()

print("Fin du jeu")
