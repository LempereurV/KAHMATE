import board
import front
import players
from color import Color
import rugbymen


Initialisation = True
Game_ON = True

while Game_ON:
    for event in front.pygame.event.get():
        ### Partie Initialisation ###
        if Initialisation:
            Graph = front.Graphique()
            P_RED = players.Player(Color.RED)
            P_BLUE = players.Player(Color.BLUE)
            front.pygame.display.flip()
            B = board.Board(Graph)
            Initialisation = False

        ### Partie Essai ###

        # Red_player_turn=True #Inutile Ici foncion initiale était de remplacer player.PLAye.can_play par un boolean
        # Blue_player_turn=not Red_player_turn

        while players.Player.can_play(P_RED):
            pos = front.Graphique.get_hitbox_for_back(Graph)

            if (not board.Board.which_rugbyman(B, pos) == False and rugbymen.Rugbyman.color(board.Board.which_rugbyman(B, pos))== Color.RED):

                # print(board.Board.which_rugbyman(B,pos))
                front.Graphique.draw_board(Graph, B)
                possible_move = board.Board.available_move_position(B, pos)
                front.Graphique.highlight_move_FElIX(Graph, possible_move)
                
                if players.Player.number_of_rugbymen(P_RED)<2:
                    pos2_or_bool=board.Board.move_rugbyman(B, pos, possible_move, Graph)
                    if not pos2_or_bool ==False :
                        print(players.Player.number_of_rugbymen(P_RED))
                        players.Player.choose_rugbymen(P_RED, board.Board.which_rugbyman(B, pos2_or_bool))
                        #print(players.Player.can_play(P_RED))
                elif board.Board.move_rugbyman(B, pos, possible_move, Graph):
                    players.Player.actualize_can_play(P_RED)
                    #print(players.Player.can_play(P_RED))
                front.Graphique.draw_board(Graph, B)
                players.Player.actualize_can_play(P_RED)


        while players.Player.can_play(P_BLUE):
            pos = front.Graphique.get_hitbox_for_back(Graph)

            if (not board.Board.which_rugbyman(B, pos) == False and rugbymen.Rugbyman.color(board.Board.which_rugbyman(B, pos))== Color.BLUE):

                # print(board.Board.which_rugbyman(B,pos))
                front.Graphique.draw_board(Graph, B)
                possible_move = board.Board.available_move_position(B, pos)
                front.Graphique.highlight_move_FElIX(Graph, possible_move)
                
                if players.Player.number_of_rugbymen(P_BLUE)<2:
                    pos2_or_bool=board.Board.move_rugbyman(B, pos, possible_move, Graph)
                    if not pos2_or_bool ==False :
                        print(players.Player.number_of_rugbymen(P_BLUE))
                        players.Player.choose_rugbymen(P_BLUE, board.Board.which_rugbyman(B, pos2_or_bool))
                        #print(players.Player.can_play(P_BLUE))
                elif board.Board.move_rugbyman(B, pos, possible_move, Graph):
                    players.Player.actualize_can_play(P_BLUE)
                    #print(players.Player.can_play(P_BLUE))
                front.Graphique.draw_board(Graph, B)
                players.Player.actualize_can_play(P_BLUE)
        
        ### Partie reset quand les deux joueurs ont joué ###
        if not players.Player.can_play(P_RED) and not players.Player.can_play(P_BLUE):
            players.Player.reset_player(P_RED)
            players.Player.reset_player(P_BLUE)
            board.Board.refresh_rugbymen_stats(B)

        if event.type == front.pygame.QUIT:
            front.pygame.quit()
            front.sys.exit()
            Game_ON = False
print("Fin du jeu")
