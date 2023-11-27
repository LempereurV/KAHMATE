import board
import front 


G=front.Graphique()

"""
PosRedRlayers=board.positions_rugbymen_player(board.Color.RED,G)
PosBluePlayers=board.positions_rugbymen_player(board.Color.BLUE,G)                          

board.Board(PosBluePlayers,PosRedRlayers)

"""

while True:
    for event in front.pygame.event.get():
        if event.type == front.pygame.MOUSEBUTTONDOWN:
            G.display_number()
            G.display_point()
            PosRedRlayers=board.positions_rugbymen_player(board.Color.RED,G)
            i=G.get_hitbox()
        if event.type == front.pygame.QUIT:
            front.pygame.quit()
            front.sys.exit()


            