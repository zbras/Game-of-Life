import pygame
from states.state import State

class PauseMenu(State):

    def __init__(self, game):

        State.__init__(self, game)

        self.game = game

    def update(self, delta_time, actions):

        if actions['tab']:
            self.exit_state()

        self.game.reset_keys()

    def render(self, display):

        self.prev_state.render(display)