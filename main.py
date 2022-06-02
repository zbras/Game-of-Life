import os
from game import Game

if __name__ == '__main__':

    os.system('cls' if os.name == 'nt' else 'clear')

    game = Game()

    while game.running:
        game.game_loop()
