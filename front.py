import pygame
import sys
import os

#Initialisation de Pygame
pygame.init()

#Chargement de l'image, chemin relatif
image_path = "Images/plateau.png"
image = pygame.image.load(image_path)
#Définition de la taille de la fenêtre
size = image.get_size()

##### TEST SPRITE #####
class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height, x, y):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.center = (x, y)
sc=50
test_block1=Block((255,0,0),10,10,sc,sc)
test_block2=Block((0,250,0),10,10,sc,sc+20)
test_block3=Block((0,0,255),10,10,sc,sc+40)
test_group=pygame.sprite.Group()
test_group.add(test_block1)
test_group.add(test_block2)
test_group.add(test_block3)

##### #####

#Création de la fenêtre
screen = pygame.display.set_mode(size)
#surf = pygame.surface.Surface(size)

print(type(screen))
#Affichage de l'image dans la fenêtre
screen.blit(image, (0, 0))

image_costaud_rouge = pygame.image.load("Images/Costaud_bleu.png")
screen.blit(image_costaud_rouge, (10, 10))
#surf.blit(image_costaud_rouge, (10, 10))

#Dessiner un point rouge
#pygame.draw.circle(screen, (255, 0, 0), (92,62), 5)

#Dessiner un point bleu
#pygame.draw.circle(screen, (0, 0, 255), (92, 107), 2)


coords=[]
for j in range(8):
    for i in range(11):
        coords.append((92+i*46.8,62+j*46.5))

#Create a hitbox for each point, each hitbox is a rectangle of 46.8*46.5 and each poinint is the superior left corner of the rectangle
hitbox=[]
for i in range(88):
    hitbox.append(pygame.Rect(coords[i][0],coords[i][1],46.8,46.5))
hitbox.append(pygame.Rect(92-46.8,62,46.8,46.5*8))
hitbox.append(pygame.Rect(92+11*46.8,62,46.8,46.5*8))

#Displays the number on the screen of the hitbox when you click on it
def display_number():
    for i in range(len(hitbox)):
        if hitbox[i].collidepoint(pygame.mouse.get_pos()):
            if i<88:
                print(i%11, i//11)
            else:
                print(i)

def get_hitbox():
    for i in range(len(hitbox)):
        if hitbox[i].collidepoint(pygame.mouse.get_pos()):
            return i

#Affiche un point rouge pour 5s quand on clique quelque part
def display_point():
    pygame.draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), 2)
    #
    test_group.draw(screen)
    #
    pygame.display.flip()
    
    screen.blit(image, (0, 0))
    pygame.time.wait(500)

    pygame.display.flip()

#Affiche un joueur au centre de la hitbox
def affiche_joueur(n_hit, path):
    joueur=pygame.image.load(path)
    joueur=pygame.transform.scale(joueur, (46.8, 46.5))
    screen.blit(joueur, coords[n_hit])
    pygame.display.flip()


#Rafraîchissement de la fenêtre
pygame.display.flip()

#Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            display_number()
            display_point()
            i=get_hitbox()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()