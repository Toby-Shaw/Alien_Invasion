import pygame
from pygame.sprite import Sprite
from UI.all_enums import AlienPattern as AP
from UI.all_enums import CollisionsStates as CS
from UI.all_enums import AlienColors as AC

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_game, color = AC.GREEN):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ap = ai_game.alien_pattern
        self.ai_game = ai_game
        self.color = color
        # Load the alien image and set its rect attribute
        if color == AC.GREEN:
            self.image = pygame.image.load("Games/Alien_Invasion/Images/alien.bmp")
        elif color == AC.RED:
            self.color = AC.RED
            self.image = pygame.image.load("Games/Alien_Invasion/Images/alien_red.bmp")
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
        elif self.ap in self.ai_game.split_rows:
            if self in self.ai_game.column1_aliens:
                self.x += (self.settings.alien_speed
                         * self.settings.column_direction_list[0])
            elif self in self.ai_game.column2_aliens:
                self.x += (self.settings.alien_speed *
                        self.settings.column_direction_list[1])
            elif self in self.ai_game.column3_aliens:
                self.x += (self.settings.alien_speed *
                        self.settings.column_direction_list[2])
            elif self in self.ai_game.column4_aliens:
                self.x += (self.settings.alien_speed *
                        self.settings.column_direction_list[3])
        self.rect.x = self.x
    
    def check_edges(self):
        """Return True if alien is at the edge of screen, or hits other aliens"""
        screen_rect = self.screen.get_rect()
        if self.ap == AP.BASIC:
            if self.rect.right >= screen_rect.right or self.rect.left <= 0:
                return CS.ONEGROUP
        elif self.ap in self.ai_game.split_rows:
            # Checks for any collisions between any of the groups
            if self in self.ai_game.column1_aliens:
                if self.rect.left <= 0:
                    return CS.FIRSTCOLUMNLEFT
                elif self.rect.right >= screen_rect.right:
                    return CS.FIRSTCOLUMNRIGHT
                elif pygame.sprite.spritecollideany(self, self.ai_game.column2_aliens):
                    return CS.FIRSTTWO
                elif pygame.sprite.spritecollideany(self, self.ai_game.column3_aliens):
                    return CS.ONETHREE
                elif pygame.sprite.spritecollideany(self, self.ai_game.column4_aliens):
                    return CS.ONEFOUR
            elif self in self.ai_game.column2_aliens:
                if self.rect.right >= screen_rect.right:
                    return CS.SECONDCOLUMNRIGHT
                elif self.rect.left <= 0:
                    return CS.SECONDCOLUMNLEFT
                elif pygame.sprite.spritecollideany(self, self.ai_game.column3_aliens):
                    return CS.TWOTHREE
                elif pygame.sprite.spritecollideany(self, self.ai_game.column4_aliens):
                    return CS.TWOFOUR
            elif self in self.ai_game.column3_aliens:
                if self.rect.right >= screen_rect.right:
                    return CS.THIRDCOLUMNRIGHT
                elif self.rect.left <= 0:
                    return CS.THIRDCOLUMNLEFT
                elif pygame.sprite.spritecollideany(self, self.ai_game.column4_aliens):
                    return CS.THREEFOUR
            elif self in self.ai_game.column4_aliens:
                if self.rect.right >= screen_rect.right:
                    return CS.FOURTHCOLUMNRIGHT
                elif self.rect.left <= 0:
                    return CS.FOURTHCOLUMNLEFT
                
    def change_color(self, new_color):
        """Change the alien color and retain previous attributes"""
        if new_color == AC.RED:
            self.image = pygame.image.load("Games/Alien_Invasion/Images/alien_red.bmp")
        elif new_color == AC.GREEN:
            self.image = pygame.image.load("Games/Alien_Invasion/Images/alien.bmp")
                    
