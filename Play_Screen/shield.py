import pygame
from pygame.sprite import Sprite

class WarpShield(Sprite):
    def __init__(self, ai_game):
        """Initialize color and all that good stuff"""
        super().__init__()
        self.ship = ai_game.ship
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.rect_width = 140
        self.rect_height = 10
        self.color = (173, 216, 230)
        self.rect = pygame.Rect(0, 0, self.rect_width, self.rect_height)

    def draw_shield(self):
        """If the powerup has been activated, draw the shield at the top of the ship"""
        if self.settings.warp_up == True:
            self.rect.centerx = self.ship.rect.centerx
            self.rect.bottom = self.ship.rect.top - 10
            self.screen.fill(self.color, self.rect)
