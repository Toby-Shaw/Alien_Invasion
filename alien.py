from re import L
import pygame
from pygame.sprite import Sprite
from alien_pattern import AlienPattern as AP
from change_speed_states import ChangeSpeedStates as CSS

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ap = ai_game.alien_pattern
        self.ai_game = ai_game

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load("Games/Alien_Invasion/Images/alien.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien to the right or left"""
        if self.ap == AP.BASIC:
            self.x += (self.settings.alien_speed * 
                        self.settings.fleet_direction)   
        # This is the same idea, just with different speeds+groups
        elif self.ap == AP.THREEROWS:
            if self in self.ai_game.column1_aliens:
                self.x += (self.settings.alien_speed
                         * self.settings.column_direction_list[0])
            elif self in self.ai_game.column2_aliens:
                self.x += (self.settings.alien_speed *
                        self.settings.column_direction_list[1])
            elif self in self.ai_game.column3_aliens:
                self.x += (self.settings.alien_speed *
                        self.settings.column_direction_list[2])
        self.rect.x = self.x
    
    def check_edges(self):
        """Return True if alien is at the edge of screen, or hits other aliens"""
        screen_rect = self.screen.get_rect()
        if self.ap == AP.BASIC:
            if self.rect.right >= screen_rect.right or self.rect.left <= 0:
                return CSS.ONEGROUP
        elif self.ap == AP.THREEROWS:
            # Checks for any collisions between any of the groups
            if self in self.ai_game.column1_aliens:
                if pygame.sprite.spritecollideany(self, self.ai_game.column2_aliens):
                    for alien in self.ai_game.column1_aliens:
                        alien.rect.x -= self.settings.alien_speed + 1
                    return CSS.FIRSTTWO
                elif pygame.sprite.spritecollideany(self, self.ai_game.column3_aliens):
                    for alien in self.ai_game.column1_aliens:
                        alien.rect.x -= self.settings.alien_speed + 1
                    return CSS.ENDTWO
                elif self.rect.left <= 0:
                    for alien in self.ai_game.column1_aliens:
                        alien.rect.x += self.settings.alien_speed + 1
                    return CSS.FIRSTCOLUMN
                elif self.rect.right >= screen_rect.right:
                    for alien in self.ai_game.column1_aliens:
                        alien.rect.x -= self.settings.alien_speed + 1
                    return CSS.FIRSTCOLUMN
            elif self in self.ai_game.column2_aliens:
                if pygame.sprite.spritecollideany(self, self.ai_game.column3_aliens):
                    for alien in self.ai_game.column2_aliens:
                        alien.rect.x -= self.settings.alien_speed + 1
                    return CSS.LASTTWO
                elif self.rect.right >= screen_rect.right:
                    for alien in self.ai_game.column2_aliens:
                        alien.rect.x -= self.settings.alien_speed + 1
                    return CSS.SECONDCOLUMN
                elif self.rect.left <= 0:
                    for alien in self.ai_game.column2_aliens:
                        alien.rect.x += self.settings.alien_speed + 1
                    return CSS.SECONDCOLUMN
            elif self in self.ai_game.column3_aliens:
                if self.rect.right >= screen_rect.right:
                    for alien in self.ai_game.column3_aliens:
                        alien.rect.x -= self.settings.alien_speed + 1
                    return CSS.THIRDCOLUMN
                elif self.rect.left <= 0:
                    for alien in self.ai_game.column3_aliens:
                        alien.rect.x += self.settings.alien_speed + 1
                    return CSS.THIRDCOLUMN

                    
