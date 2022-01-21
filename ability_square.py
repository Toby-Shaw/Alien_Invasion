import pygame.font

class AbilityButton:

    def __init__(self, ai_game, msg, offset):
        """Initialize the attributes of the button"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and color of the button
        self.width, self.height = 50, 50
        self.button_color = (86, 91, 203)
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 48)
        self.covering = False

        # Build the rect object and put it a bit to the side of the score
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.right = (ai_game.sb.score_rect.left - offset)
        self.rect.top = 15

        # Need to prep the message as well
        self._prep_caption(msg)

    def _prep_caption(self, msg):
        """Turn the msg into a rendered caption and center it on the square"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_ability_square(self):
        """Draw blank square then center the message on it"""
        self.screen.fill(self.button_color, self.rect)
        if not self.covering:
            self.screen.blit(self.msg_image, self.msg_image_rect)
