import pygame.ftfont

class Text:

    def __init__(self, ai_game, text, font_size, font_color, posx, posy, line_spacing = 40):
        """Initialize the text's attributes"""
        pygame.ftfont.init()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.posx = posx
        self.posy = posy
        self.font_color = font_color
        self.font = pygame.ftfont.SysFont(None, font_size)

        self._prep_text(text, line_spacing)

    def _prep_text(self, text, line_spacing = 40):
        """Turn text into a rendered image and place it at the positions given"""
        # Fix \n issues before they occur
        neat_text = text.replace("\n       ", "")
        # Split where double-spaced
        self.text_lines = neat_text.split("  ")
        self.text_list = []
        self.text_rect_list = []
        counter = 0
        for line in self.text_lines:
            # Get the image for each individual line
            self.text_list.append(self.font.render(line, True, self.font_color, self.settings.bg_color))
        for image in self.text_list:
            # Get the rect for each individual image
            self.text_rect_list.append(image.get_rect())
        for rect in self.text_rect_list:
            # Move all the rects to the correct spots
            rect.centerx = self.posx
            rect.centery = self.posy + (line_spacing * counter)
            counter += 1

    def draw_text(self):
        "Draw the text onto the screen"
        for i in range(len(self.text_list)):
            # Use the correct image and rect for each line
            self.screen.blit(self.text_list[i], self.text_rect_list[i])