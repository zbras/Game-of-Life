import pygame, time, os, json
from states.title_menu import TitleMenu
from states.pause_menu import PauseMenu

class Game():

    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Game of Life Concept')
        pygame.mouse.set_visible(False)
        infoObject = pygame.display.Info()

        self.screen_width, self.screen_height = infoObject.current_w, infoObject.current_h
        self.board = False
        self.assets_dir = os.path.join('assets')
        self.font_dir = os.path.join(self.assets_dir, 'fonts')
        self.running, self.playing = True, True
        self.delta_time, self.prev_time = 0, 0
        self.surface = pygame.Surface((self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.NOFRAME)
        self.actions = {
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

            if self.actions['escape']:
                self.exit_game()

            self.update()
            self.render()
            self.reset_keys()

    def get_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                self.state_stack[-1].process_mouse_down(position)

            elif event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                self.state_stack[-1].process_mouse_up(position)

    def update(self):

        self.state_stack[-1].update(self.delta_time, self.actions)

    def render(self):

        self.state_stack[-1].render(self.surface)
        pygame.display.flip()

    def get_delta_time(self):

        now = time.time()
        self.delta_time = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, color, x, y, size):

        self.font = pygame.font.Font(os.path.join(self.font_dir, 'PressStart2P-Regular.ttf'), size)
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def load_assets(self):

        pass

    def load_states(self):

        self.title_screen = TitleMenu(self)
        self.state_stack.append(self.title_screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def load_config(self):

        with open('settings/config.json', 'r') as f:
            config = json.load(f)

        return config

    def save_config(self):

        with open('settings/config.json', 'w') as f:
            json.dump(self.board.options, f, indent = 4)

    def exit_game(self):

        self.save_config()
        self.running, self.playing = False, False

        quit()

if __name__ == '__main__':
    quit()
