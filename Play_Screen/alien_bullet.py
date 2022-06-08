from cmath import sqrt
import pygame
from pygame.sprite import Sprite
import math

class AlienBullet(Sprite):
    """A class to manage bullets fired from the alien fleet/boss"""

    def __init__(self, ai_game, alien, homing=False):
        """Create a bullet object at the alien's current position."""
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.alien_bullet_color
        self.homing = homing
        self.down = round(-1/2*math.pi, 3)
        self.cap_angle = 0.03
        self.previous_angle = 0

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, 
                self.settings.alien_bullet_width, self.settings.alien_bullet_height)
        self.rect.midtop = alien.rect.midbottom

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)
        self._update_coords()
        self.x = float(self.rect.x)

    def update(self, speed = 4.4):
        """Move the bullet up the screen"""
        if not self.homing:
            # Update the decimal position of the bullet.
            self.y += speed
        else:
            self._update_coords()
            self._determine_attack_path()
            self._move_one_step()
        # Update the rect position.
        self.rect.y = self.y

    def draw_alien_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def _determine_attack_path(self):
        self.x_distance = self.target_coords[0] - self.coords[0]
        self.y_distance = self.target_coords[1] - self.coords[1]
        if self.x_distance != 0:
            self.path_length = round(sqrt(self.x_distance**2 + self.y_distance**2).real, 3)
            self.angle_of_attack = round(math.asin(self.x_distance/self.path_length), 4)
            #print(self.angle_of_attack)
        else:
            self.path_length = self.y_distance
            self.angle_of_attack = self.down
        if self.previous_angle: 
            if self.angle_of_attack - self.previous_angle > self.cap_angle:
                self.angle_of_attack = self.previous_angle + self.cap_angle
            elif self.angle_of_attack - self.previous_angle < self.cap_angle:
                self.angle_of_attack = self.previous_angle - self.cap_angle
            if abs(self.angle_of_attack) > 0.75:
                self.angle_of_attack = self.previous_angle
        self.previous_angle = self.angle_of_attack

    def _move_one_step(self):
        self.vertical_movement = math.cos(self.angle_of_attack) * self.settings.alien_bullet_speed
        self.horizontal_movement = math.sin(self.angle_of_attack) * self.settings.alien_bullet_speed
        self.x += self.horizontal_movement
        self.y += self.vertical_movement
        self.rect.x = self.x
        self.rect.y = self.y

    def _update_coords(self):
        self.coords = self.rect.center
        self.ship_coords = self.ai_game.ship.rect.midtop
        self.target_coords = [self.ship_coords[0], self.ship_coords[1]+25]