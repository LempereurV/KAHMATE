import board
import front 





Initialisation=True
Game_ON=True

while Game_ON:
    for event in front.pygame.event.get():
        ### Partie Initialisation ###
        if Initialisation:
            G=front.Graphique()
            front.pygame.display.flip() 
            B=board.Board(G)
            Initialisation=False

        ### Partie Essai ###
        pos=front.Graphique.get_hitbox_for_back(G)
        print(board.Board.which_rugbyman(B,pos))

        
        if event.type == front.pygame.QUIT:
            front.pygame.quit()
            front.sys.exit()
            Game_ON=False
print("Fin du jeu")
    
            




            