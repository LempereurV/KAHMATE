import pygame
import actions

class FloatingMenu(pygame.sprite.Sprite):
    # Class of floating menus, from which token actions can be selected

    def __init__(
        self,
        rows,
        pos=(0, 0),
        font_size=15,
        font_type="Comic Sans MS",
        color_bg=(255, 255, 255),
        color_font=(0, 0, 0),
    ):
        ### FloatingMenu attribut ###
        #  size_menu : Number of rows in the menu
        #  interline : Distance between two rows (in px)
        #  border : Distance to the horizontal borders of the menu
        #  font_size : Size of the font
        #  image : surface of the background menu sprite (see pygame.sprite.Sprite)
        #  rect : hitbox and position of the background menu sprite (see pygame.sprite.Sprite)
        #  availability : boolean table, each value gives the availability of the associated row
        #  rows : surface table, containing for each row its surface
        #  rows_rect : rect table, containing for each row its rect
        super().__init__()

        # Dimension attributes
        self.size_menu = len(rows)
        self.interline = 2
        self.border = 5
        self.font_size = font_size
        width = int(font_size * max([len(x) for x in rows]) / 1.5)
        height = 2 * self.border + (font_size + self.interline) * self.size_menu

        # Sprite attributes
        self.image = pygame.Surface([width, height])
        self.image.fill(color_bg)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        # Menu attributes
        self.availability = [
            True for i in range(self.size_menu)
        ]  # for each row, false if the option is not available
        self.rows = [None for i in range(self.size_menu)]
        self.rows_rect = [None for i in range(self.size_menu)]
        menu_font = pygame.font.SysFont(
            font_type, font_size
        )  # rows and rows_rect initialisation
        for i in range(self.size_menu):
            self.rows[i] = menu_font.render(rows[i], False, color_font)
            self.rows_rect[i] = self.rows[i].get_rect()
            self.rows_rect[i].x = self.border + self.rect.x
            self.rows_rect[i].y = self.rect.y + self.border + (self.font_size) * i

    def get_pos(self):
        # Return menu position un a tuple, which corresponds to it's upper left border position
        return (self.rect.x, self.rect.y)

    def is_on_screen(self, screen_size):
        # Return True if the menu is on screen, False overwise
        if (
            self.rect.x < screen_size[0]
            and self.rect.y < screen_size[1]
            and self.rect.x > 0
            and self.rect.y > 0
        ):
            return True
        return False

    def update_rows_pos(self):
        # Update the rows positions accordingly to the menu background
        for i in range(self.size_menu):
            self.rows_rect[i].x = self.border + self.rect.x
            self.rows_rect[i].y = self.rect.y + self.border + (self.font_size) * i

    def move(self, pos):
        # Move the menu
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.update_rows_pos()

    def move_next_to_case(self, pos, coords):
        # Move the table next to the cases of index pos=(x, y) (x, y are the index in coords)
        self.move(coords[actions.coord_to_hitbox((pos[0] + 1, pos[1]))])

    def draw(self, screen):
        # Display on scren the menu
        screen.blit(self.image, (self.rect.x, self.rect.y))
        for i in range(self.size_menu):
            screen.blit(self.rows[i], (self.rows_rect[i].x, self.rows_rect[i].y))

    def get_collision(self):
        #  Check and return hitbox collision with the mouse (None if no hibox collided, # of the hitbox collided overwise)
        for i in range(self.size_menu):
            if self.rows_rect[i].collidepoint(pygame.mouse.get_pos()):
                print(i)
                return i
        print(None)
        return None

    def is_option_available(self, id_option):
        # Return True if the option is available, False overwise
        for i in range(self.size):
            if i == id_option:
                return self.availability[i]
        return None  # The id of the selected option does not correspond to the menu size (should never be triggered in normal use)
