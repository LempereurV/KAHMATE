import front
import players
from color import Color
import rugbymen
<<<<<<< HEAD
import actions
import game
=======
import game
import actions 

>>>>>>> branche_de_felix2


### Initializations ###

<<<<<<< HEAD
        ### Partie Essai ###

        # Red_player_turn=True #Inutile Ici foncion initiale était de remplacer player.PLAye.can_play par un boolean
        # Blue_player_turn=not Red_player_turn

        while players.Player.can_play(P_RED):
            pos = front.Graphique.get_hitbox_for_back(Graph)

            if (
                not board.Board.which_rugbyman(B, pos) == False
                and rugbymen.Rugbyman.color(board.Board.which_rugbyman(B, pos))
                == Color.RED
            ):
                # print(board.Board.which_rugbyman(B,pos))
                front.Graphique.draw_board(Graph, B)
                possible_move = board.Board.available_move_position(B, pos)
                front.Graphique.highlight_move_FElIX(Graph, possible_move)

                if players.Player.number_of_rugbymen(P_RED) < 2:
                    pos2_or_bool = board.Board.move_rugbyman(
                        B, pos, possible_move, Graph
                    )
                    if not pos2_or_bool == False:
                        print(players.Player.number_of_rugbymen(P_RED))
                        players.Player.choose_rugbymen(
                            P_RED, board.Board.which_rugbyman(B, pos2_or_bool)
                        )
                        # print(players.Player.can_play(P_RED))
                front.Graphique.draw_board(Graph, B)
                players.Player.actualize_can_play(P_RED)

        while players.Player.can_play(P_BLUE):
            pos = front.Graphique.get_hitbox_for_back(Graph)

            if (
                not board.Board.which_rugbyman(B, pos) == False
                and rugbymen.Rugbyman.color(board.Board.which_rugbyman(B, pos))
                == Color.BLUE
            ):
                # print(board.Board.which_rugbyman(B,pos))
                front.Graphique.draw_board(Graph, B)
                players.Player.choose_rugbymen(
                    P_BLUE, board.Board.which_rugbyman(B, pos)
                )
=======
#The Graph 
Graph = front.Graphique()
Game=game.Game(Graph)
Graph.display_ball(Game.get_ball())
front.pygame.display.flip()
Initialisation = False




#This the main loop of the game, the function is_game_over of game is verifying each turn if one rugbyman is in the adversary camp
>>>>>>> branche_de_felix2


<<<<<<< HEAD
                if board.Board.move_rugbyman(B, pos, possible_move, Graph):
                    players.Player.actualize_can_play(P_BLUE)
                    # print(players.Player.can_play(P_BLUE))
                front.Graphique.draw_board(Graph, B)

        ### Partie reset quand les deux joueurs ont joué ###
        if not players.Player.can_play(P_RED) and not players.Player.can_play(P_BLUE):
            players.Player.reset_player(P_RED)
            players.Player.reset_player(P_BLUE)
            board.Board.refresh_rugbymen_stats(B)
=======
while not Game.is_game_over():

    active_player = Game.get_player_turn()

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
>>>>>>> branche_de_felix2

print("Fin du jeu")
