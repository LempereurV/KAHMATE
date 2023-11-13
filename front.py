from typing import Any
import pygame
import sys

# Initialisation de Pygame
pygame.init()

clock = pygame.time.Clock()

#Chargement de l'image, chemin relatif
image_path = "Images/plateau.png"
image = pygame.image.load(image_path)
# Définition de la taille de la fenêtre
size = image.get_size()


##### TEST SPRITE #####

class PlayerTokens(pygame.sprite.Sprite):
    def __init__(self, picture_path, scale_x=46.8, scale_y=46.5):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.image = pygame.transform.scale(self.image, (scale_x, scale_y))
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.center = pygame.mouse.get_pos()



##### #####

# Création de la fenêtre
screen = pygame.display.set_mode(size)
#surf = pygame.surface.Surface(size)

print(type(screen))
#Affichage de l'image dans la fenêtre
screen.blit(image, (0, 0))

image_costaud_rouge = pygame.image.load("Images/Costaud_bleu.png")
screen.blit(image_costaud_rouge, (10, 10))
#surf.blit(image_costaud_rouge, (10, 10))

# Dessiner un point rouge
# pygame.draw.circle(screen, (255, 0, 0), (92,62), 2)

# Dessiner un point bleu
# pygame.draw.circle(screen, (0, 0, 255), (92, 107), 2)


coords = []
for j in range(8):
    for i in range(11):
        coords.append((92 + i * 46.8, 62 + j * 46.5))

# Hitbox de chaque point
hitbox = []
for i in range(88):
    hitbox.append(pygame.Rect(coords[i][0], coords[i][1], 46.8, 46.5))
hitbox.append(pygame.Rect(92 - 46.8, 62, 46.8, 46.5 * 8))
hitbox.append(pygame.Rect(92 + 11 * 46.8, 62, 46.8, 46.5 * 8))

class Graphique:
    def __init__(self):
        # Initialisation de Pygame
        pygame.init()

        # Chargement de l'image, chemin relatif
        image_path = "Images/plateau.png"
        self.plateau = pygame.image.load(image_path)
        # Définition de la taille de la fenêtre
        self.size = self.plateau.get_size()

        # Création de la fenêtre
        self.screen = pygame.display.set_mode(self.size)
        # Affichage de l'image dans la fenêtre
        self.screen.blit(self.plateau, (0, 0))

    # Displays the number on the screen of the hitbox when you click on it
    def display_number(self):
        for i in range(len(hitbox)):
            if hitbox[i].collidepoint(pygame.mouse.get_pos()):
                if i < 88:
                    print(i % 11, i // 11)
                else:
                    print(i)

    def get_hitbox(self):
        for i in range(len(hitbox)):
            if hitbox[i].collidepoint(pygame.mouse.get_pos()):
                if i<88:
                    return [i,(i%11, i//11)]
                else:
                    return [i]

    # Affiche un point rouge pour 5s quand on clique quelque part
    def display_point(self):
        pygame.draw.circle(self.screen, (255, 0, 0), pygame.mouse.get_pos(), 2)
        pygame.display.flip()
        pygame.time.wait(500)
        self.screen.blit(self.plateau, (0, 0))
        pygame.display.flip()

    # Affiche un joueur au centre de la hitbox
    def affiche_joueur(self, n_hit, path):
        joueur = pygame.image.load(path)
        joueur = pygame.transform.scale(joueur, (46.8, 46.5))
        self.screen.blit(joueur, coords[n_hit])
        pygame.display.flip()

    #Met en surbrillance les cases où le joueur peut se déplacer
    def highlight_move(self, list_move):
        for i in range(len(list_move)):
            pygame.draw.circle(self.screen, (20, 255, 167), (coords[list_move[i]][0]+46.8/2,coords[list_move[i]][1]+46.5/2),10)
        pygame.display.flip()

    def create_dropdown_menu(self, options, menu_pos, menu_size):
        self.menu_options = options
        self.menu_rect = pygame.Rect(menu_pos, menu_size)
        self.menu_open = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_rect.collidepoint(event.pos):
                self.menu_open = not self.menu_open
            elif self.menu_open:
                for i, option in enumerate(self.menu_options):
                    if pygame.Rect(self.menu_rect.x, self.menu_rect.y + (i+1)*self.menu_rect.height, self.menu_rect.width, self.menu_rect.height).collidepoint(event.pos):
                        print(f"You clicked {option}")
                        self.menu_open = False

    def draw_menu(self):
        if self.menu_open:
            for i, option in enumerate(self.menu_options):
                pygame.draw.rect(self.screen, (255, 255, 255), (self.menu_rect.x, self.menu_rect.y + (i+1)*self.menu_rect.height, self.menu_rect.width, self.menu_rect.height))
                self.screen.blit(pygame.font.Font(None, 32).render(option, True, (0, 0, 0)), (self.menu_rect.x, self.menu_rect.y + (i+1)*self.menu_rect.height))

    # Rafraîchissement de la fenêtre
    def refresh(self):
        pygame.display.flip()

    # Boucle principale
    def main_loop(self):
        # Players tokens sprites initialisation

        playertoken = PlayerTokens("Images/Costaud_bleu.png")
        tokens_group = pygame.sprite.Group()
        tokens_group.add(playertoken)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.display_number()
                    self.display_point()
                    i=self.get_hitbox()[0]
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()
        screen.blit(image, (0, 0))
        tokens_group.draw(screen)
        tokens_group.update() # For now, the sprites in tokens_group just follow the mouse (could eventually be used to make Tokens follow the mouse while moving them)
        clock.tick(60)

if __name__ == "__main__":
    graph = Graphique()
    graph.main_loop()
