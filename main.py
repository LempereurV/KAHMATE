import board
import front
import players
from color import Color
import rugbymen
import actions
import game

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

            if (
                not board.Board.which_rugbyman(B, pos) == False
                and rugbymen.Rugbyman.color(board.Board.which_rugbyman(B, pos))
                == Color.RED
            ):
                # print(board.Board.which_rugbyman(B,pos))
                front.Graphique.draw_board(Graph, B)
                players.Player.choose_rugbymen(
                    P_RED, board.Board.which_rugbyman(B, pos)
                )
                possible_move = board.Board.available_move_position(B, pos)
                front.Graphique.highlight_move_FElIX(Graph, possible_move)

                if board.Board.move_rugbyman(B, pos, possible_move, Graph):
                    players.Player.actualize_can_play(P_RED)
                    # print(players.Player.can_play(P_RED))
                    front.Graphique.draw_board(Graph, B)
                else:
                    front.Graphique.draw_board(Graph, B)

        while players.Player.can_play(P_BLUE):
            pos = front.Graphique.get_hitbox_for_back(Graph)

            if (
                not board.Board.which_rugbyman(B, pos) == False
                and rugbymen.Rugbyman.color(board.Board.which_rugbyman(B, pos))
                == Color.BLUE
            ):
                # print(board.Board.which_rugbyman(B,pos))
                front.Graphique.draw_board(Graph, B)
                possible_move = board.Board.available_move_position(B, pos)
                # print(possible_move)
                front.Graphique.highlight_move_FElIX(Graph, possible_move)

                if board.Board.move_rugbyman(B, pos, possible_move, Graph):
                    players.Player.actualize_can_play(P_BLUE)
                    front.Graphique.draw_board(Graph, B)
                else:
                    front.Graphique.draw_board(Graph, B)
        ### Partie reset quand les deux joueurs ont joué ###
        if not players.Player.can_play(P_RED) and not players.Player.can_play(P_BLUE):
            players.Player.set_can_play(P_RED, True)
            players.Player.set_can_play(P_BLUE, True)
            board.Board.refresh_rugbymen_stats(B)

        if event.type == front.pygame.QUIT:
            front.pygame.quit()
            front.sys.exit()
            Game_ON = False
print("Fin du jeu")
