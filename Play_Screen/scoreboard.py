import pygame.font
import pygame
from pygame.sprite import Group
from Play_Screen.ship import Ship
from UI.text import Text
from UI.all_enums import GameStates as GS


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
        #self.initials_defined = False
        self.bypass = False
        self.defined_initials = ''
        self.go_ahead = False
        self.letter_number = 0
        self.letter_texts = []
        self.horizontal_spacing = 7
        self.alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.displayed_high_score = self.stats.high_score[0]
        self.edited = False

        # Prep the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_high_scores()

    def prep_score(self):
        """Turn the score into an image"""
        self.stats.score = round(self.stats.score, -1)
        score_str = ("Score: " + "{:,}".format(self.stats.score))
        self.score_image = self.font.render(score_str, True, 
            self.text_color, self.settings.bg_color)
    
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into an image."""
        high_score = round(self.displayed_high_score, -1)
        high_score_str = ("Highscore: " + "{:,}".format(high_score))
        self.high_score_image = self.font.render(high_score_str, True, 
                self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top - 10

    def check_high_score(self):
        """Check for a new high score"""
        if self.stats.score > self.displayed_high_score:
            self.displayed_high_score = self.stats.score
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
        """Render the highscores on the HIGHSCORES page, in descending order"""
        self.high_text = ""
        for x in range(len(self.stats.high_score)):
            self.high_text += f"{x + 1} : {self.stats.high_initials[x]} - {self.stats.high_score[x]}  "
        self.high_score_text = Text(self.ai_game, self.high_text, 60, (0, 0, 0), 
                    400, 275, line_spacing=80, alignment = 0)
        self.high_score_title_text = Text(self.ai_game, "Highscores: ", 120, (0, 0, 0), 
                    600, 150)

    def _go_to_input(self, beat_high_score):
        """Moves to INPUT page and saves the index of the beaten score, then gets the title"""
        #print('moving to input page since a score was beaten')
        self.ai_game.stats.game_layer = GS.INPUTPAGE
        self.temp_index = self.stats.high_score.index(beat_high_score)
        self.ai_game.input_text._prep_text(f"Congrats! Your score is #{self.temp_index + 1}  Your Name:")

    def _write_high_score(self):
        """Convert the high score list back into file format, to be saved between games"""
        high_score = open("Games/Alien_Invasion/high_score.txt", "w")
        write_out = ""
        for x in range(len(self.stats.high_score)):
            write_out += (str(self.stats.high_score[x]) + ' ')
        write_out += '/ '
        for x in range(len(self.stats.high_initials)):
            write_out += self.stats.high_initials[x] + ' '
        high_score.write(write_out)

    def _move_initials_and_scores(self):
        """Move all later initial forward to match their scores"""
        if self.temp_index != 4 and self.temp_index != 0:
            self.stats.high_score = (self.stats.high_score[:self.temp_index] + 
                [self.stats.score] + self.stats.high_score[self.temp_index:-1])
            self.stats.high_initials = (self.stats.high_initials[:self.temp_index] + 
                [self.defined_initials] + self.stats.high_initials[self.temp_index:-1])
        elif self.temp_index == 4:
            self.stats.high_score[4] = self.stats.score
            self.stats.high_initials[4] = self.defined_initials
        elif self.temp_index == 0:
            self.stats.high_score = [self.stats.score] + self.stats.high_score[:-1]
            self.stats.high_initials = [self.defined_initials] + self.stats.high_initials[:-1]
        self.edited = True
        self.defined_initials = ""

    def show_high_scores(self):
        """Draw the highscore things on the page"""
        self.high_score_title_text.draw_text()
        self.high_score_text.draw_text()
    
    def finish_updating_high_scores(self):
        """To be called every frame on INPUTPAGE, finishes input things"""
        if self.go_ahead:
            self.go_ahead = False
            self._move_initials_and_scores()
            self._write_high_score()
            self.ai_game.stats.game_layer = GS.MAINMENU
            self.letter_texts = []
    
    def _check_inputs(self, event):
        """Based on the inputs, draw and add the letters"""
        if event.__dict__['unicode'] in self.alphabet and event.__dict__['unicode'] and len(self.defined_initials) < 10:
            self.defined_initials += event.__dict__['unicode']
            self.letter_texts.append(Text(self.ai_game, self.defined_initials[self.letter_number], 
                80, (0, 0, 0), 400, 450))
            if self.letter_number > 0:
                self.letter_texts[self.letter_number].text_rect_list[0].x = (
                    self.letter_texts[self.letter_number - 1].text_rect_list[0].right + self.horizontal_spacing)
            self._update_total_length()
            self.letter_number += 1
        elif event.key == pygame.K_BACKSPACE and self.letter_number > 0:
            self.letter_number -= 1
            self.letter_texts.pop(-1)
            self.defined_initials = self.defined_initials[:-1]
            self._update_total_length()
        elif event.__dict__['key'] == 13 and len(self.defined_initials) >= 2:
            # This works for the enter key
            self.letter_number = 0
            self.go_ahead = True
    
    def _update_total_length(self):
        self.total_length = 0
        for letter in self.letter_texts:
            self.total_length += letter.text_rect_list[0].width
            if letter != self.letter_texts[-1]:
                self.total_length += self.horizontal_spacing
        print(self.total_length)