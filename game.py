import rugbymen
import players
import random


class Game:
    def __init__(self):
        player1 = players.Player()
        player2 = players.Player()
        ball = players.Ball(random.randint(1, 8))

    def is_over(self):
        pass

    def play(self):
        while not self.is_over:
            pass
