import board
import front 
import players
from color import Color





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
        pos=front.Graphique.get_hitbox_for_back(Graph)
        print(board.Board.which_rugbyman(B,pos))
        front.Graphique.draw_board(Graph,B)
        print(board.Board.available_moove_position(B,pos))
        front.Graphique.highlight_move(Graph,board.Board.available_moove_position(B,pos))
            

        
        if event.type == front.pygame.QUIT:
            front.pygame.quit()
            front.sys.exit()
            Game_ON=False
print("Fin du jeu")
    
            




            