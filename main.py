import os
from tkinter import Tk
from game import Game

if __name__ == '__main__':

    os.system('cls' if os.name == 'nt' else 'clear')

    root = Tk()
    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()
    game = Game(screen_width, screen_height)

    while game.running:
        game.game_loop()
