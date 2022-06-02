import pygame

class Slider():

    def __init__(self, game, name, alias, val, val_min, val_max, x_pos, y_pos):

        self.alias = alias
        self.game = game
        self.val = val
        self.val_min = val_min
        self.val_max = val_max
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.surface = pygame.surface.Surface((150, 50))
        self.hit = False
        self.transparent = (1, 1, 1)
        self.font = pygame.font.SysFont("Verdana", 12)

        self.surface.set_colorkey(self.transparent)
        self.surface.fill((self.transparent))
        self.txt_surface = self.font.render(name, 1, (255, 255, 255))
        self.txt_rect = self.txt_surface.get_rect()

        pygame.draw.rect(self.surface, (255, 255, 255), [10, 26, 80, 14], 0, border_radius = 8)

        self.surface.blit(self.txt_surface, self.txt_rect)

        self.button_surface = pygame.surface.Surface((16, 16))
        self.button_surface.fill((1, 1, 1))
        self.button_surface.set_colorkey((1, 1, 1))
        pygame.draw.circle(self.button_surface, (100, 100, 100), (8, 8), 8)

    def draw(self):

        surface = self.surface.copy()
        pos = (10 + int((self.val - self.val_min) / (self.val_max - self.val_min) * 80), 33)
        self.button_rect = self.button_surface.get_rect(center = pos)

        surface.blit(self.button_surface, self.button_rect)
        self.button_rect.move_ip(self.x_pos, self.y_pos)
        self.game.screen.blit(surface, (self.x_pos, self.y_pos))

    def move(self):

        self.val = (pygame.mouse.get_pos()[0] - self.x_pos - 10) / 80 * (self.val_max - self.val_min) + self.val_min
        if self.val < self.val_min:
            self.val = self.val_min
        if self.val > self.val_max:
            self.val = self.val_max

        overwrite_settings = [f'{p}_{s}' for p in ['r', 'g', 'b', 'a'] for s in ['min', 'max']]

        if self.alias in overwrite_settings:
            if self.alias[3:] != 'max' and int(self.val) > self.game.board.options[f'{self.alias[:1]}_max']['val']:
                self.game.board.options[f'{self.alias[:1]}_max']['val'] = int(self.val)
            elif int(self.val) < self.game.board.options[f'{self.alias[:1]}_min']['val']:
                self.game.board.options[f'{self.alias[:1]}_min']['val'] = int(self.val)

        self.game.board.options[self.alias]['val'] = int(self.val)