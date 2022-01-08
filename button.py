import pygame.font

class Button:

    def __init__(self, ai_game, msg, button_color, posx, posy):
        """Initialize the button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.button_color = button_color

        # Set dimensions and properties of the button
        self.rect_height = 50
        self.rect_width = 200
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.rect_width, self.rect_height)
        self.rect.centerx = posx
        self.rect.centery = posy

        # The button message needs to be prepped once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)