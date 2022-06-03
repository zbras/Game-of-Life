import pygame
from states.state import State
from states.slider import Slider

class PauseMenu(State):

    def __init__(self, game):

        State.__init__(self, game)

        pygame.mouse.set_visible(True)

        self.game = game
        self.sliders = []

        x, y = self.game.screen_width - 170, 100

        for option in self.game.board.options:
            y += 60
            self.sliders.append(
                Slider(
                    self.game,
                    option,
                    self.game.board.options[option]['alias'],
                    self.game.board.options[option]['val'],
                    self.game.board.options[option]['min'],
                    self.game.board.options[option]['max'],
                    x,
                    y
                )
            )

        for slider in self.sliders:
            slider.draw()

    def update(self, delta_time, actions):

        if actions['tab']:
            self.exit_state()

    def process_mouse_down(self, position):

        for slider in self.sliders:
            if slider.button_rect.collidepoint(position):
                slider.hit = True

    def process_mouse_up(self, position):

        for slider in self.sliders:
            slider.hit = False

    def exit_state(self):

        pygame.mouse.set_visible(False)

        return super().exit_state()

    def render(self, display):

        self.prev_state.render(self.game.screen)
        self.background = pygame.Surface((self.game.screen_width, self.game.screen_height))
        self.background.set_alpha(200)
        self.background.fill((0, 0, 0))
        self.game.screen.blit(self.background, (0, 0))

        self.game.draw_text(self.game.screen, '- Paused -', (255, 255, 255), self.game.screen_width / 2, self.game.screen_height / 2, 30)

        for slider in self.sliders:
            if slider.hit:
                slider.move()
            slider.draw()


if __name__ == '__main__':
    quit()
