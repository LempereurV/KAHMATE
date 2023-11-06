import rugbymen
import players
import random


number_of_columns = 8

class Game:
    def __init__(self):
        player1 = players.Player("blue")
        player2 = players.Player("red")
        ball = players.Ball(random.randint(1,number_of_columns))

    def is_over(self):
        pass

    def players(self):
        return self.player1.players() + self.player2.players()

    def play(self):
        while not self.is_over:
            pass


