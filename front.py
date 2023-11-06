import pygame
import sys

pygame.init()

# Chargement de l'image
image = pygame.image.load("Images/plateau.png")

# Définition de la taille de la fenêtre
size = image.get_size()

# Création de la fenêtre
screen = pygame.display.set_mode(size)

# Affichage de l'image dans la fenêtre
screen.blit(image, (0, 0))

# Dessiner un point rouge
pygame.draw.circle(screen, (255, 0, 0), (92, 62), 2)

# Dessiner un point bleu
pygame.draw.circle(screen, (0, 0, 255), (92, 107), 2)

# Rafraîchissement de la fenêtre
pygame.display.flip()

while True:
    """
    Main loop that waits for events and handles them.
    If the event is the closing of the window, the program quits.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
