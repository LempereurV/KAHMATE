import rugbymen
from constants import Constants
from color import Color
import front 

def norm(pos1,pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

def norm2(pos1,pos2):
    return (pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2



def placement_orders(color):
    """
    Returns the dictionary of the placement orders of the rugbymen during game initialization
    """
    R = {
        "First Normal Rugbyman": rugbymen.Rugbyman(color),
        "Second Normal Rugbyman": rugbymen.Rugbyman(color),
        "Strong Rugbyman": rugbymen.StrongRugbyman(color),
        "Hard Rugbyman": rugbymen.HardRugbyman(color),
        "Smart Rugbyman": rugbymen.SmartRugbyman(color),
        "Fast Rugbyman": rugbymen.FastRugbyman(color),
    }
    return R


def positions_rugbymen_player(placement_order, graphic):

    i = 0
    n_rugbymen = len(placement_order)
    R = [None] * n_rugbymen 
    L_pos=[]
    Noms = list(placement_order.keys())  
    color=placement_order[Noms[0]].get_color()
    

    """
    if color == Color.RED:
        placement_order[Noms[0]].set_pos_x(Constants.number_of_rows//2)
        placement_order[Noms[0]].set_pos_y(Constants.number_of_columns // 2-1)
        R[0]=placement_order[Noms[0]]
        graphic.display_rugbyman(R[0])
        

        placement_order[Noms[1]].set_pos_x(Constants.number_of_rows//2+1)
        placement_order[Noms[1]].set_pos_y(Constants.number_of_columns // 2-1)
        R[1]=placement_order[Noms[1]]
        graphic.display_rugbyman(R[1])

        placement_order[Noms[2]].set_pos_x(Constants.number_of_rows//2)
        placement_order[Noms[2]].set_pos_y(Constants.number_of_columns // 2)
        R[2]=placement_order[Noms[2]]
        graphic.display_rugbyman(R[2])

        placement_order[Noms[3]].set_pos_x(Constants.number_of_rows//2+1)
        placement_order[Noms[3]].set_pos_y(Constants.number_of_columns // 2)
        R[3]=placement_order[Noms[3]]
        graphic.display_rugbyman(R[3])

        placement_order[Noms[4]].set_pos_x(Constants.number_of_rows//2-1)
        placement_order[Noms[4]].set_pos_y(Constants.number_of_columns // 2)
        R[4]=placement_order[Noms[4]]
        graphic.display_rugbyman(R[4])

        placement_order[Noms[5]].set_pos_x(Constants.number_of_rows//2+2)
        placement_order[Noms[5]].set_pos_y(Constants.number_of_columns // 2)
        R[5]=placement_order[Noms[5]]
        graphic.display_rugbyman(R[5])
        
        

    else:

        for i in range(n_rugbymen):
            placement_order[Noms[i]].set_pos_x(i+1)
            placement_order[Noms[i]].set_pos_y(7)

            R[i]=placement_order[Noms[i]]
            graphic.display_rugbyman(R[i])
    front.pygame.display.flip()
    
    return R
    
    
    """
    
    
    while i < n_rugbymen:
        # The Color.split(".")[-1] is for the color to display as intended
        print( str(color).split(".")[-1] + " Player, Choose the position of the " + Noms[i])

        # Fonction de la classe graphique qui renvoie une liste de la forme [i,j] avec i et j les colonnes et lignes de la case cliquée
        pos,_ = graphic.get_hitbox_on_click()


        #graphic.draw_board_init(R[:i])
        

        if pos in L_pos:
            cond_pos_already_taken = True
            while cond_pos_already_taken:
                print("The position chosen is already taken, re choose the position")
                pos,cond = graphic.get_hitbox_on_click()
                if not pos in L_pos:
                    cond_pos_already_taken = False

        if (color == Color.RED 
            and (pos[1] > Constants.number_of_columns // 2
            or pos[1]==0)):  # Red characters should be placed on the left
            cond_RED = True
            while cond_RED:
                print("The position isn't correct, the red team is suppose to be on the left of the field")
                pos,cond = graphic.get_hitbox_on_click()
                if pos[1] < Constants.number_of_columns // 2+1 and pos[1]!=0:
                    cond_RED = False

        if (color == Color.BLUE 
            and (pos[1] <= Constants.number_of_columns // 2+1
            or pos[1]==Constants.number_of_columns+1)):  # Blue characters should be placed on the right
            cond_Blue = True
            while cond_Blue:
                print("The position isn't correct, the blue team is suppose to be on the right, re choose the position")
                pos,cond = graphic.get_hitbox_on_click()
                if pos[1] > Constants.number_of_columns // 2+1 and pos[1]!=Constants.number_of_columns+1:
                    cond_Blue = False
        
        #Toutes les conditions ont été vérifiées, on peut enregistrer les informations
        placement_order[Noms[i]].set_pos(pos)
        #graphique.display_rugbyman(placement_order[Noms[i]])  # Display the newly placed rugbymen on the board
        R[i] =  placement_order[Noms[i]]
        L_pos.append(pos)
        graphic.display_rugbyman(R[i])
        front.pygame.display.flip()
        i += 1
    return R
