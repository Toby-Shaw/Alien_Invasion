import pygame.font

class AbilityButton:

    def __init__(self, ai_game, msg, offset):
        """Initialize the attributes of the button"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.ai_game = ai_game

        # Set the dimensions and color of the button
        self.width, self.height = 50, 50
        self.button_color = (86, 91, 203)
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 60)
        self.covering = False
        self.msg = msg

        # Set the cooldown stage to 0, other cooldown things
        self.cooldown_stage = 0
        self.cooldown_start = False
        self.cooldown_up = True
        self.cooldown = 0

        # Cooldown things, split the rect button into 50 rects to bring into 
        # foreground or background according to cooldown
        self.number_of_slices = 50
        self.rect_list = []
        for x in range(self.number_of_slices):
            self.rect_list.append(pygame.Rect(0, 0, self.width, self.height / self.number_of_slices))
        for y in range(len(self.rect_list)):
            self.rect_list[y].right = (ai_game.sb.score_rect.left - offset)
            self.rect_list[y].top = 15 + (self.height / self.number_of_slices * y)

        # Need to prep the message as well
        self._prep_caption()

    def _prep_caption(self):
        """Turn the msg into a rendered caption and center it on the square"""
        self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect_list[self.number_of_slices // 2].center

    def _cooldown(self):
        """If told to start the cooldown, shift things and count accordingly"""
        if self.cooldown_start:
            if self.cooldown == 0:
                self.cooldown += 1
                self.button_color = (200, 200, 200)
                self._prep_caption()
            elif self.cooldown < 900:
                self.cooldown += 1
                self.cooldown_up = False
                self.cooldown_stage = self.cooldown // 18
            else:
                self._reset_cooldown()

    def _reset_cooldown(self):
        """Reset the variables related to cooldown"""
        self.cooldown_start = False
        self.cooldown = 0
        self.cooldown_up = True
        self.covering = False
        self.cooldown_stage = 0
        self.button_color = (86, 91, 203)
        self._prep_caption()

    def draw_ability_square(self):
        """Draw blank square then center the message on it"""
        if self.covering:
            # If cooldown, draw the appropriate layers under the letter
            for rect in range(0, self.cooldown_stage):
                self.screen.fill(self.button_color, self.rect_list[rect])
            self.screen.blit(self.msg_image, self.msg_image_rect)
            # Then draw all the ones that are still on top
            for rect in range(self.cooldown_stage, self.number_of_slices):
                self.screen.fill(self.button_color, self.rect_list[rect])
        else:
            # Otherwise just draw them all under the letter
            for rect in range(self.number_of_slices):
                self.screen.fill(self.button_color, self.rect_list[rect])
            self.screen.blit(self.msg_image, self.msg_image_rect)
