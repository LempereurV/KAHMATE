import pygame
import sys
import os

# Initialisation de Pygame
pygame.init()

# Chargement de l'image, chemin relatif
image_path = "images/plateau.png"
image = pygame.image.load(image_path)
# Définition de la taille de la fenêtre
size = image.get_size()

# Création de la fenêtre
screen = pygame.display.set_mode(size)
# Affichage de l'image dans la fenêtre
screen.blit(image, (0, 0))

# Dessiner un point rouge
# pygame.draw.circle(screen, (255, 0, 0), (92,62), 2)

# Dessiner un point bleu
# pygame.draw.circle(screen, (0, 0, 255), (92, 107), 2)


coords = []
for j in range(8):
    for i in range(11):
        coords.append((92 + i * 46.8, 62 + j * 46.5))

# Create a hitbox for each point, each hitbox is a rectangle of 46.8*46.5 and each poinint is the superior left corner of the rectangle
hitbox = []
for i in range(88):
    hitbox.append(pygame.Rect(coords[i][0], coords[i][1], 46.8, 46.5))
hitbox.append(pygame.Rect(92 - 46.8, 62, 46.8, 46.5 * 8))
hitbox.append(pygame.Rect(92 + 11 * 46.8, 62, 46.8, 46.5 * 8))


# Displays the number on the screen of the hitbox when you click on it
def display_number():
    for i in range(len(hitbox)):
        if hitbox[i].collidepoint(pygame.mouse.get_pos()):
            if i < 88:
                print(i % 11, i // 11)
            else:
                print(i)


def get_hitbox():
    for i in range(len(hitbox)):
        if hitbox[i].collidepoint(pygame.mouse.get_pos()):
            return i


# Affiche un point rouge pour 5s quand on clique quelque part
def display_point():
    pygame.draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), 2)
    pygame.display.flip()
    pygame.time.wait(500)
    screen.blit(image, (0, 0))
    pygame.display.flip()


# Affiche un joueur au centre de la hitbox
def affiche_joueur(n_hit, path):
    joueur = pygame.image.load(path)
    joueur = pygame.transform.scale(joueur, (46.8, 46.5))
    screen.blit(joueur, coords[n_hit])
    pygame.display.flip()


# Rafraîchissement de la fenêtre
pygame.display.flip()

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            display_number()
            display_point()
            i = get_hitbox()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
