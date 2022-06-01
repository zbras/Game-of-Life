import pygame, time, os
from states.title_menu import TitleMenu

class Game():

    def __init__(self, screen_width, screen_height):

        pygame.init()
        pygame.mouse.set_visible(False)

        self.running, self.playing = True, True
        self.delta_time, self.prev_time = 0, 0
        self.screen_width, self.screen_height = screen_width, screen_height
        self.canvas = pygame.Surface((screen_width, screen_height))
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
        self.actions = {
            'left': False,
            'right': False,
            'up': False,
            'down': False,
            'tab': False,
            'escape': False,
            'start': False
        }
        self.state_stack = []

        self.load_assets()
        self.load_states()

    def game_loop(self):

        while self.playing:
            self.get_delta_time()
            self.get_events()
            self.update()
            self.render()

            if self.actions['escape']:
                self.running, self.playing = False, False
                quit()

    def get_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.actions['tab'] = True

                if event.key == pygame.K_ESCAPE:
                    self.actions['escape'] = True

                if event.key == pygame.K_RETURN:
                    self.actions['start'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_TAB:
                    self.actions['tab'] = False

                if event.key == pygame.K_ESCAPE:
                    self.actions['escape'] = False

                if event.key == pygame.K_RETURN:
                    self.actions['start'] = False

    def update(self):

        self.state_stack[-1].update(self.delta_time, self.actions)

    def render(self):

        self.state_stack[-1].render(self.canvas)
        pygame.display.flip()

    def get_delta_time(self):

        now = time.time()
        self.delta_time = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, color, x, y):

        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def load_assets(self):

        self.assets_dir = os.path.join('assets')
        self.font_dir = os.path.join(self.assets_dir, 'fonts')
        self.font = pygame.font.Font(os.path.join(self.font_dir, 'PressStart2P-Regular.ttf'), 30)

    def load_states(self):

        self.title_screen = TitleMenu(self)
        self.state_stack.append(self.title_screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

if __name__ == '__main__':
    quit()
