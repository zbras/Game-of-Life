import sys, time, pygame, os
from tkinter import Tk
from collections import defaultdict
from copy import deepcopy
from math import ceil, floor
from random import randint

class Board():

    def __init__(self, screen_width, screen_height):

        #   Programmable settings
        self.RED_MAX, self.GREEN_MAX, self.BLUE_MAX = 255, 255, 255
        self.RED_MIN, self.GREEN_MIN, self.BLUE_MIN = 255, 255, 255
        self.CELL_MINIMUM = 20
        self.BORDER_SIZE = 1
        self.REGEN_PERCENT = .005
        self.TIME_BETWEEN_SEQUENCES = .1

        #   Static settings
        self.GRID_UPDATE_ITERATIONS = 0
        self.OFFSCREEN_CHILDREN_REMOVED = 0
        self.OFFSETS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        self.X_CELLS, self.Y_CELLS = ceil((screen_width / screen_height)) * self.CELL_MINIMUM, ceil((screen_height / screen_width)) * self.CELL_MINIMUM
        self.CELL_WIDTH = (screen_width) / self.X_CELLS
        self.CELL_HEIGHT = (screen_height) / self.Y_CELLS
        self.RANDOM_CELL_REGEN_COUNT = ceil(self.REGEN_PERCENT * (self.X_CELLS * self.Y_CELLS))

        self.generate_new_board_state()

    def generate_new_board_state(self):

        self.CELLS = set()

        for i in range(0, floor((self.X_CELLS * self.Y_CELLS) / 5), 1):
            x, y = randint(0, self.X_CELLS), randint(0, self.Y_CELLS)
            self.CELLS.add((x, y))

    def get_neighbors(self, x, y):

        neighboring_candidates = {(x + x_add, y + y_add) for x_add, y_add in self.OFFSETS}
        alive_neighbors = {(pos[0], pos[1]) for pos in neighboring_candidates if pos in self.CELLS}

        return alive_neighbors, neighboring_candidates.difference(alive_neighbors)

    def add_random_alive_cells(self):

        added_cells = set()

        for i in range(self.RANDOM_CELL_REGEN_COUNT):
            x = randint(0, self.X_CELLS)
            y = randint(0, self.Y_CELLS)
            self.CELLS.add((x, y))
            added_cells.add((x, y))

        return added_cells

    def remove_offscreen_tiles(self):

        cell_container = deepcopy(self.CELLS)

        for (x, y) in cell_container:
            if (x > self.X_CELLS + 1 or
                x < -1 or
                y > self.Y_CELLS + 1 or
                y < -1):
                self.CELLS.discard((x, y))
                self.OFFSCREEN_CHILDREN_REMOVED += 1

    def update_grid(self):

        if len(self.CELLS) < self.RANDOM_CELL_REGEN_COUNT:
            self.generate_new_board_state()

        added_cells = self.add_random_alive_cells()
        new_cells = deepcopy(self.CELLS)
        births = defaultdict(int)

        for (x, y) in self.CELLS:
            alive_neighbors, dead_neighbors = self.get_neighbors(x, y)

            if len(alive_neighbors) not in [2, 3]:
                new_cells.remove((x, y))

            for pos in dead_neighbors:
                births[pos] += 1

        for pos, _ in filter(lambda e: e[1] == 3, births.items()):
            new_cells.add((pos[0], pos[1]))

        self.CELLS = deepcopy(new_cells)

        if 'added_cells' in locals():
            for (x, y) in added_cells:
                self.CELLS.discard((x, y))

        self.GRID_UPDATE_ITERATIONS += 1
        self.remove_offscreen_tiles()

def update_screen(screen, b) -> None:

    for (x, y) in b.CELLS:
        pygame.draw.rect(
            screen,
            (randint(b.RED_MIN, b.RED_MAX), randint(b.GREEN_MIN, b.GREEN_MAX), randint(b.BLUE_MIN, b.BLUE_MAX)),
            (x * b.CELL_WIDTH + b.BORDER_SIZE, y * b.CELL_HEIGHT + b.BORDER_SIZE, b.CELL_WIDTH - b.BORDER_SIZE, b.CELL_HEIGHT - b.BORDER_SIZE)
        )

def main():

    os.system('cls' if os.name == 'nt' else 'clear')

    root = Tk()
    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()

    pygame.init()
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
    board = Board(screen.get_width(), screen.get_height())

    while True:
        if pygame.QUIT in [e.type for e in pygame.event.get()]:
            print(f'Removed {board.OFFSCREEN_CHILDREN_REMOVED} alive offscreen nodes over {board.GRID_UPDATE_ITERATIONS} sequences.')
            sys.exit(0)

        screen.fill((0, 0, 0))
        update_screen(screen, board)
        board.update_grid()
        pygame.display.flip()
        time.sleep(board.TIME_BETWEEN_SEQUENCES)

if __name__ == "__main__":
    main()