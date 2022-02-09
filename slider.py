from pygame.rect import Rect
import pygame

class Slider:

    def __init__(self, ai_game, color, posx, posy, id):
        """Initialize the slider"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.color = color
        self.bg_rect = Rect(0, 0, 300, 30)
        self.second_rect = Rect(0, 0, 294, 24)
        self.bg_rect.centerx = posx
        self.bg_rect.centery = posy
        self.second_rect.center = self.bg_rect.center
        self.crossbar_bg = Rect(0, 0, 30, 60)
        self.crossbar_front = Rect(0, 0, 24, 54)
        self.crossbar_bg.right = self.bg_rect.right
        self.crossbar_bg.centery = self.bg_rect.centery
        self.crossbar_front.center = self.crossbar_bg.center
        self.clicked = False
        self.previous_value = 1
        self.id = id

    def update(self, mouse_pos, new_click):
        """Update the slider position"""
        # If it was just clicked and colliding, or the mouse hasn't come up yet, update
        if (self.crossbar_bg.collidepoint(mouse_pos) and new_click) or self.clicked:
            self.clicked = True
            if mouse_pos[0] <= (self.bg_rect.right - 15) and mouse_pos[0] >= (self.bg_rect.left + 15):
                self.crossbar_bg.centerx = mouse_pos[0] 
            elif mouse_pos[0] < self.bg_rect.left:
                self.crossbar_bg.left = self.bg_rect.left
            elif mouse_pos[0] > self.bg_rect.right:
                self.crossbar_bg.right = self.bg_rect.right
            self.crossbar_front.center = self.crossbar_bg.center
            if mouse_pos[0] != self.previous_value:
                self.update_statistic((self.crossbar_bg.left - self.bg_rect.left) / 300)
            self.previous_value = mouse_pos[0]

    def update_statistic(self, present_value):
        """Change the volume based on the slider id"""
        if self.id == 0:
            pygame.mixer.music.set_volume(present_value)
        elif self.id == 1:
            self.ai_game.game_sounds.sound_channel.set_volume(present_value)

    def _draw_slider(self):
        """Draw all four rectangles"""
        self.screen.fill((0, 0, 0), self.bg_rect)
        self.screen.fill(self.color, self.second_rect)
        self.screen.fill((0, 0, 0), self.crossbar_bg)
        self.screen.fill(self.color, self.crossbar_front)

