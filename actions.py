#Fonction qui traduit coordonnées en numéro de hitbox
def coord_to_hitbox(coord):
    return coord[0]+11*coord[1]

def hitbox_to_coord(n_hit):
    return (n_hit%11, n_hit//11)