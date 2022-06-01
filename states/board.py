import pygame, time
from collections import defaultdict
from copy import deepcopy
from math import ceil, floor
from random import randint
from states.state import State
from states.pause_menu import PauseMenu

class Board(State):

    def __init__(self, game):

        State.__init__(self, game)

        #   Programmable settings
        self.cell_minimum = 20
        self.border_size = 1
        self.time_between_sequences = .1
        self.regen_board_when_empty = True
        self.regen_percent_of_population = .005
        self.brightness_min, self.brightness_max = 255, 255
        self.red_max, self.green_max, self.blue_max = 255, 0, 100
        self.red_min, self.green_min, self.blue_min = 0, 0, 20

        #   Static settings
        self.game = game
        self.offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        self.x_cells = ceil((self.game.screen_width / self.game.screen_height)) * self.cell_minimum
        self.y_cells = ceil((self.game.screen_height / self.game.screen_width)) * self.cell_minimum
        self.cell_width = (self.game.screen_width) / self.x_cells
        self.cell_height = (self.game.screen_height) / self.y_cells
        self.random_cell_regen_count = ceil(self.regen_percent_of_population * (self.x_cells * self.y_cells))

        self.generate_new_board_state()

    def generate_new_board_state(self) -> None:
        '''
        Generates a new board state of living cells, randomly assigning locations for the cells.
        The population of the new board state can have up to a maximum of 1/5 of the total amount of living and dead cells.
        '''

        self.cells = set()

        for i in range(0, floor((self.x_cells * self.y_cells) / 5), 1):
            x, y = randint(0, self.x_cells), randint(0, self.y_cells)
            self.cells.add((x, y))

    def get_neighbors(self, x, y) -> dict:
        '''
        Given a living cell's coordinates, this function looks at the cell's surrounding neighbors and categorizes them as either alive or dead.

        Returns:
            dict() of alive neighbors
            dict() of dead neighbors
        '''

        neighboring_cells = {(x + x_add, y + y_add) for x_add, y_add in self.offsets}
        alive_neighbors = {(pos[0], pos[1]) for pos in neighboring_cells if pos in self.cells}

        return alive_neighbors, neighboring_cells.difference(alive_neighbors)

    def regenerate_cells(self) -> set:
        '''
        Regenerates a user-defined number of cells in random locations.
        This function is utilized to extend the lifetime of the entire population, and prevent static pockets of cells from regenerating the entire population when it is necessary to do so.

        Returns:
            set() of cells that have been regenerated
        '''

        regenerated_cells = set()

        for i in range(self.random_cell_regen_count):
            x = randint(0, self.x_cells)
            y = randint(0, self.y_cells)
            self.cells.add((x, y))
            regenerated_cells.add((x, y))

        return regenerated_cells

    def remove_offscreen_cells(self) -> None:
        '''
        Removes cells which are located two cells away from the edge of the screen.
        This function is used to conserve memory and prevent gliders from generating pockets of cells offscreen.
        '''

        cell_container = deepcopy(self.cells)

        for (x, y) in cell_container:
            if (x > self.x_cells + 1 or
                x < -1 or
                y > self.y_cells + 1 or
                y < -1):
                self.cells.discard((x, y))

    def update(self, delta_time, actions) -> None:
        '''
        Updates the cell locations after resetting the board (if necessary), regenerating cells, applying the rules of John Conway's Game of Life, and removing offscreen cells.
        '''

        if actions['tab']:
            new_state = PauseMenu(self.game)
            new_state.enter_state()

        if self.regen_board_when_empty == True and len(self.cells) < self.random_cell_regen_count:
            self.generate_new_board_state()

        regenerated_cells = self.regenerate_cells()
        new_cells = deepcopy(self.cells)
        births = defaultdict(int)

        for (x, y) in self.cells:
            alive_neighbors, dead_neighbors = self.get_neighbors(x, y)

            if len(alive_neighbors) not in [2, 3]:
                new_cells.remove((x, y))

            for pos in dead_neighbors:
                births[pos] += 1

        for pos, _ in filter(lambda e: e[1] == 3, births.items()):
            new_cells.add((pos[0], pos[1]))

        self.cells = deepcopy(new_cells)

        for (x, y) in regenerated_cells:
            self.cells.discard((x, y))

        self.remove_offscreen_cells()
        self.render_sequence()
        self.game.reset_keys()

        pygame.time.delay(ceil(self.time_between_sequences * 1000))

    def render_sequence(self):
        '''
        Redraws and refreshes the screen.
        '''

        self.game.screen.fill((0, 0, 0))

        for (x, y) in self.cells:
            brightness = randint(self.brightness_min, self.brightness_max) / 255
            pygame.draw.rect(
                self.game.screen,
                (randint(ceil(self.red_min * brightness), ceil(self.red_max * brightness)), randint(ceil(self.green_min * brightness), ceil(self.green_max * brightness)), randint(ceil(self.blue_min * brightness), ceil(self.blue_max * brightness))),
                (x * self.cell_width + self.border_size, y * self.cell_height + self.border_size, self.cell_width - self.border_size, self.cell_height - self.border_size)
            )

if __name__ == '__main__':
    quit()
