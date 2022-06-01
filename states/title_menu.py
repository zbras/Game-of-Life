from states.state import State
from states.board import Board

class TitleMenu(State):

    def __init__(self, game):

        State.__init__(self, game)

    def update(self, delta_time, actions):

        if actions['start']:
            new_state = Board(self.game)
            new_state.enter_state()

        self.game.reset_keys()

    def render(self, display):

        self.game.screen.blit(self.game.canvas, (0, 0))
        self.game.draw_text(display, 'Game of Life', (255, 255, 255), self.game.screen_width / 2, self.game.screen_height / 2)

if __name__ == '__main__':
    quit()
