import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition de la taille de la fenêtre
size = (800, 600)

# Création de la fenêtre
screen = pygame.display.set_mode(size)

# Chargement de l'image
image = pygame.image.load("Documents/KAHMATE/Images/plateau.png")

# Affichage de l'image dans la fenêtre
screen.blit(image, (0, 0))

# Dessiner un point rouge
pygame.draw.circle(screen, (255, 0, 0), (92, 62), 2)

# Dessiner un point bleu
pygame.draw.circle(screen, (0, 0, 255), (92, 107), 2)

# Rafraîchissement de la fenêtre
pygame.display.flip()

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
