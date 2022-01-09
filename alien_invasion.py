import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import Gamestats
from button import Button
from scoreboard import Scoreboard
from ability_square import AbilityButton
from text import Text

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics,
        # and make a scoreboard
        self.stats = Gamestats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the Play button and other buttons
        self.play_button = Button(self, "Play", (0, 255, 0),
            (self.settings.screen_width / 2), (self.settings.screen_height / 2))
        self.main_menu = Button(self, "Main Menu", (0, 255, 0), 
            (self.settings.screen_width / 2), self.settings.screen_height / 2 + 120)
        self.resume = Button(self, "Resume", (0, 255, 0),
            (self.settings.screen_width / 2), (self.settings.screen_height / 2))

        # Make the title + Pause text
        self.title = Text(self, "Alien Invasion", 110, (0, 255, 0), 
            (self.settings.screen_width / 2), 180)
        self.pause = Text(self, "Paused", 110, (0, 255, 0),
            (self.settings.screen_width / 2), 180)

        # Make the Ability "strong bullet"
        self.ability_square = AbilityButton(self, "S")

        # Start Alien Invasion in an inactive state.
        self.stats.dict_of_states = {'main menu' : 1, 'play' : 2, 'pause' : 3}
        self.stats.game_layer = 1

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_layer == 2:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._strong_bullet_cooldown()
            self._update_screen()

    def _start_game(self):
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_layer = 2
        self.settings.initialize_dynamic_settings()
        self.ability_square.covering = False
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()  

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)  

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                high_score = open("/home/toby/Pythonthings/Games/Alien_Invasion/high_score.txt", "w")
                high_score.write(str(self.stats.high_score))
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_pause_buttons(mouse_pos)
                self._check_main_buttons(mouse_pos)
                

    def _check_main_buttons(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.game_layer == 1:
            # Reset the game settings.
            self._start_game()

    def _check_pause_buttons(self, mouse_pos):
        """Check pause screen buttons"""
        if self.stats.game_layer == 3:
            button_clicked1 = self.main_menu.rect.collidepoint(mouse_pos)
            if button_clicked1:
                # Return to the main menu if clicked
                self.stats.game_layer = 1
                self._update_screen()
            elif self.resume.rect.collidepoint(mouse_pos):
                # Return to the game if clicked
                self.stats.game_layer = 2
                self._update_screen()

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_s:
            if self.settings.normal_bullet and self.settings.cooldown_up:
                self.settings.strong_bullet()
                self.ability_square.covering = True
        elif event.key == pygame.K_q:
            if self.stats.game_layer == 2:
                self.stats.game_layer = 3
                pygame.mouse.set_visible(True)
            elif self.stats.game_layer == 3:
                high_score = open("/home/toby/Pythonthings/Games/Alien_Invasion/high_score.txt", "w")
                high_score.write(str(self.stats.high_score))
                self.stats.game_layer = 1
                pygame.mouse.set_visible(True)
            else:
                high_score = open("/home/toby/Pythonthings/Games/Alien_Invasion/high_score.txt", "w")
                high_score.write(str(self.stats.high_score))
                sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            self._strong_bullet_timer()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet position
        self.bullets.update()

        # Get rid of bullets that are out of bounds
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _strong_bullet_timer(self):
        """Tracks strong bullet usage, resets once it passes threshold"""
        if not self.settings.normal_bullet:
            self.settings.strong_bullets_fired += 1
            # Checks number of strong bullets, discontinues if necessary
            if self.settings.strong_bullets_allowed < self.settings.strong_bullets_fired:
                self.settings.normal_bullet_reset()
                self.settings.cooldown_start = True

    def _strong_bullet_cooldown(self):
        """If strong bullet just ended, starts cooldown"""
        if self.settings.cooldown_start == True:
            if self.settings.cooldown < 1100:
                self.settings.cooldown += 1
                self.settings.cooldown_up = False
            elif self.settings.cooldown >= 1100:
                self.settings.cooldown_start = False
                self.settings.cooldown = 0
                self.settings.cooldown_up = True
                self.ability_square.covering = False

    
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(
        self.bullets, self.aliens, self.settings.normal_bullet, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points*len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self._new_level()

    def _new_level(self):
        """ Destroy existing bullets and create new fleet. """
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()
        self.settings.cooldown_start = False
        self.settings.cooldown = 0
        self.settings.cooldown_up = True
        self.ability_square.covering = False

        # Increase level
        self.stats.level += 1
        self.sb.prep_level()

        # Stop strong bullet if active
        if self.settings.normal_bullet == False:
            self.settings.normal_bullet_reset() 

    def _ship_hit(self):
        """Respond to the ship being hit by alien"""
        if self.stats.ships_left > 0:
            # Decrement ships left, and update graphics.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Reset strong bullet
            if not self.settings.normal_bullet:
                self.settings.normal_bullet_reset()
            self.ability_square.covering = False
            self.settings.cooldown_start = False
            self.settings.cooldown = 0
            self.settings.cooldown_up = True

            # Slow it down marginally
            self.settings.ship_speed *= 0.9
            self.settings.alien_speed *= 0.9
            self.settings.bullet_speed *= 0.9

            # Pause.
            sleep(1)
        else:
            self.stats.game_layer = 1
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """
        Check if the fleet is at an edge, 
          then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Make an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                    (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create a alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond if an aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat it as if a ship got hit.
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_play_screen(self):
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score info and ability square
        self.sb.show_score()
        self.ability_square.draw_ability_square()
        
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        # Draw the play screen when appropriate
        if self.stats.game_layer == 2:
            self._update_play_screen()
            
        # Draw the main menu when appropriate.
        elif self.stats.game_layer == 1:
            self.title.draw_text()
            self.play_button.draw_button()
            
        # Draw the puase screen when appropriate
        elif self.stats.game_layer == 3:
            self.pause.draw_text()
            self.main_menu.draw_button()
            self.resume.draw_button()
        
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
