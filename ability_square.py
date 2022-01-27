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

        # Set the cooldown stage to 0
        self.cooldown_stage = 0

        # Build the rect object and put it a bit to the side of the score
        #self.rect = pygame.Rect(0, 0, self.width, self.height)
        #self.rect.right = (ai_game.sb.score_rect.left - offset)
        #self.rect.top = 15
        # Trying a new thing for cooldown purposes
        self.number_of_slices = 50
        self.rect_list = []
        for x in range(self.number_of_slices):
            self.rect_list.append(pygame.Rect(0, 0, self.width, self.height / self.number_of_slices))
        for y in range(len(self.rect_list)):
            self.rect_list[y].right = (ai_game.sb.score_rect.left - offset)
            self.rect_list[y].top = 15 + (self.height / self.number_of_slices * y)

        # Need to prep the message as well
        self._prep_caption(msg)

    def _prep_caption(self, msg):
        """Turn the msg into a rendered caption and center it on the square"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect_list[self.number_of_slices // 2].center

    def draw_ability_square(self):
        """Draw blank square then center the message on it"""
        #self.screen.fill(self.button_color, self.rect)
        for rect in range(len(self.rect_list)):
            self.screen.fill(self.button_color, self.rect_list[rect])
        if not self.covering:
            self.screen.blit(self.msg_image, self.msg_image_rect)
