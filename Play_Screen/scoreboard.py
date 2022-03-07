import pygame.font
from pygame.sprite import Group
from Play_Screen.ship import Ship
from UI.text import Text

class Scoreboard:
    """A class to report scoring info."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attribs."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #Font settings for scoring info
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 36)

        # Prep the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_high_scores()

    def prep_score(self):
        """Turn the score into an image"""
        rounded_score = round(self.stats.score, -1)
        score_str = ("Score: " + "{:,}".format(rounded_score))
        self.score_image = self.font.render(score_str, True, 
            self.text_color, self.settings.bg_color)
    
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into an image."""
        high_score = round(self.stats.high_score[0], -1)
        high_score_str = ("Highscore: " + "{:,}".format(high_score))
        self.high_score_image = self.font.render(high_score_str, True, 
                self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top - 10

    def check_high_score(self):
        """Check for a new high score"""
        if self.stats.score > self.stats.high_score[0]:
            self.stats.high_score[0] = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Turn the level into an image."""
        level_str = ("Level: " + str(self.stats.level))
        self.level_image = self.font.render(level_str, True, 
                self.text_color, self.settings.bg_color)

        #Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw score (and level (and ships)) to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
    
    def show_ships(self):
        """Draw the life number of ships"""
        self.ships.draw(self.screen)

    def prep_high_scores(self):
        """Render the highscores"""
        self.high_text = ""
        for x in range(len(self.stats.high_score)):
            self.high_text += f"{x + 1} : {self.stats.high_score[x]}  "
        self.high_score_text = Text(self.ai_game, self.high_text, 60, (0, 0, 0), 
                    400, 275, line_spacing=80, alignment = 0)
        self.high_score_title_text = Text(self.ai_game, "Highscores: ", 120, (0, 0, 0), 
                    500, 150)

    def _update_high_scores_page(self):
        """Open the high score file and add the new high scores"""
        for x in self.stats.high_score:
            if self.stats.score > x:
                temp_index = self.stats.high_score.index(x)
                for y in range(len(self.stats.high_score) - 2, self.stats.high_score.index(x) - 1, -1):
                    self.stats.high_score[y + 1] = self.stats.high_score[y]
                self.stats.high_score[temp_index] = self.stats.score
                break
        high_score = open("Games/Alien_Invasion/high_score.txt", "w")
        write_out = ""
        for x in range(len(self.stats.high_score)):
            write_out += (str(self.stats.high_score[x]) + ' ')
        high_score.write(write_out)
    
    def show_high_scores(self):
        """Draw the highscore things on the page"""
        self.high_score_title_text.draw_text()
        self.high_score_text.draw_text()