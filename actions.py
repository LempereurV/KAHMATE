class Actions: 

    def moove_up(self):
            self.posy += 1

        def moove_down(self):
            self.posy -= 1

        def moove_left(self):
            self.posx -= 1

        def moove_right(self):
            self.posx += 1

        def tackle(self, card_self, other, card_other):
            if (
                self.active == True
                and self.possesion == False
                and self.posx == other.posx
                and self.posy == other.posy
            ):
                if (self.attack_bonus + card_self.point) > (
                    other.defense_bonus + card_other.point
                ):
                    other.active = False
                    return True
            return False

        def push_through(self, card_self, other, card_other):
            if (
                self.active == True
                and self.possesion == True
                and self.posx == other.posx
                and self.posy == other.posy
            ):
                if (self.attack_bonus + card_self.point) > (
                    other.defense_bonus + card_other.point
                ):
                    other.active = False
                    return True
            return False

        def grubber_kick(self, throw):
            if self.possesion == True:
                return True
            else:
                return False

        def place_rugbyman(self, x, y):
            self.posx = x
            self.posy = y