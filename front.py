import pygame
import sys
import os

#Initialisation de Pygame
pygame.init()

#Définition de la taille de la fenêtre
size = (800, 600)

#Création de la fenêtre
screen = pygame.display.set_mode(size)

#Chargement de l'image
image_path = "C:/Users/Ponts/Documents/KAHMATE/Images/plateau.png"
image = pygame.image.load(image_path)

#Affichage de l'image dans la fenêtre
screen.blit(image, (0, 0))

#Dessiner un point rouge
#pygame.draw.circle(screen, (255, 0, 0), (92,62), 2)

#Dessiner un point bleu
#pygame.draw.circle(screen, (0, 0, 255), (92, 107), 2)


coords=[(92,62)]
for i in range(11):
    for j in range(8):
        coords.append((92+i*46.8,62+j*46.5))

#Create a hitbox for each point, each hitbox is a rectangle of 46.8*46.5 and each poinint is the superior left corner of the rectangle
hitbox=[]
for i in range(88):
    hitbox.append(pygame.Rect(coords[i][0],coords[i][1],46.8,46.5))

#Displays the number on the screen of the hitbox when you click on it
def display_number(hitbox):
    for i in range(88):
        if hitbox[i].collidepoint(pygame.mouse.get_pos()):
            print(i)
            font = pygame.font.Font(None, 250)

#Affiche un point rouge pour 5s quand on clique quelque part
def display_point():
    pygame.draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), 2)
    pygame.display.flip()
    pygame.time.wait(500)
    screen.blit(image, (0, 0))
    pygame.display.flip()


#Rafraîchissement de la fenêtre
pygame.display.flip()

#Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            display_number(hitbox)
            display_point()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()