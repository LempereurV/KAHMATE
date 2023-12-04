import board
import front 
import players
from color import Color
import rugbymen




Initialisation=True
Game_ON=True

while Game_ON:
    for event in front.pygame.event.get():
        ### Partie Initialisation ###
        if Initialisation:
            Graph=front.Graphique()
            P_RED=players.Player(Color.RED)
            P_BLUE=players.Player(Color.BLUE)
            front.pygame.display.flip() 
            B=board.Board(Graph)
            Initialisation=False

        ### Partie Essai ###

        Red_player_turn=True
        Blue_player_turn=not Red_player_turn

        while Red_player_turn:
            pos=front.Graphique.get_hitbox_for_back(Graph)

            if not board.Board.which_rugbyman(B,pos)==False and rugbymen.Rugbyman.color(board.Board.which_rugbyman(B,pos))==Color.RED:
                print(board.Board.which_rugbyman(B,pos))
                front.Graphique.draw_board(Graph,B)
                possible_move=board.Board.available_moove_position(B,pos)
                front.Graphique.highlight_move_FElIX(Graph,possible_move) 

                if board.Board.moove_rugbyman(B,pos,possible_move,Graph):
                    Red_player_turn=False
                    Blue_player_turn=True
                    front.Graphique.draw_board(Graph,B)  
            #else :
                #print(board.Board.which_rugbyman(B,pos))
        while Blue_player_turn:
            pos=front.Graphique.get_hitbox_for_back(Graph)

            if not board.Board.which_rugbyman(B,pos)==False and rugbymen.Rugbyman.color(board.Board.which_rugbyman(B,pos))==Color.BLUE:
                print(board.Board.which_rugbyman(B,pos))
                front.Graphique.draw_board(Graph,B)
                possible_move=board.Board.available_moove_position(B,pos)
                front.Graphique.highlight_move_FElIX(Graph,possible_move) 

                if board.Board.moove_rugbyman(B,pos,possible_move,Graph):
                    Red_player_turn=True
                    Blue_player_turn=False
                    front.Graphique.draw_board(Graph,B)  
            #else :
                #print(board.Board.which_rugbyman(B,pos))
            
            

        
        if event.type == front.pygame.QUIT:
            front.pygame.quit()
            front.sys.exit()
            Game_ON=False
print("Fin du jeu")
    
            




            