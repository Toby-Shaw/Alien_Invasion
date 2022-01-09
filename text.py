import pygame.font

class Text:

    def __init__(self, ai_game, text, font_size, font_color, posx, posy):
        """Initialize the text's attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.posx = posx
        self.posy = posy
        self.font_color = font_color
        self.font = pygame.font.SysFont(None, font_size)

        self._prep_text(text)

    def _prep_text(self, text):
        """Turn text into a rendered image and place it at the positions given"""
        self.text_image = self.font.render(text, True, self.font_color, self.settings.bg_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.centerx = self.posx
        self.text_image_rect.centery = self.posy

    def draw_text(self):
        "Draw the text onto the screen"
        self.screen.blit(self.text_image, self.text_image_rect)