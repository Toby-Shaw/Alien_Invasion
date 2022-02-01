from ast import Pass
import sys
from time import sleep
import random
import os

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
from alien_bullet import AlienBullet
from shield import WarpShield
from game_states import GameStates as GS
from alien_pattern import AlienPattern as AP
from change_speed_states import ChangeSpeedStates as CSS

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
        # for AP.THREEROWS only
        self.column1_aliens = pygame.sprite.Group()
        self.column2_aliens = pygame.sprite.Group()
        self.column3_aliens = pygame.sprite.Group()
        self.three_columns_group = [self.column1_aliens, self.column2_aliens, self.column3_aliens]
        # Alien bullet group
        self.alien_bullets = pygame.sprite.Group()
        # Create the warp shield
        self.warp_shield = WarpShield(self)

        # Make the Play button and other buttons
        self.play_button = Button(self, "Play", (0, 255, 0),
            (self.settings.screen_width / 2), (self.settings.screen_height / 2))
        self.main_menu = Button(self, "Main Menu", (0, 255, 0), 
            (self.settings.screen_width / 2), self.settings.screen_height / 2 + 100)
        self.resume = Button(self, "Resume", (0, 255, 0),
            (self.settings.screen_width / 2), (self.settings.screen_height / 2))
        self.info = Button(self, "Information", (0, 255, 0), 
            self.settings.screen_width / 2, (self.settings.screen_height / 2 + 100))

        # Make the title + Pause text
        self.title = Text(self, "Alien Invasion", 110, (0, 255, 0), 
            (self.settings.screen_width / 2), 180)
        self.pause = Text(self, "Paused", 110, (0, 255, 0),
            (self.settings.screen_width / 2), 180)

        # Make the Information text pieces
        self.strong_bullet_info = Text(self, 
        """Strong Bullet is an activatable ability that
        allows your bullets to  pierce multiple enemies.
        Activate it with the down key or S""", 
            40, (0, 0, 0), 550, 100)
        self.shield_info = Text(self, 
        """Warp Shield is an activatable ability that
        blocks up to two bullets  from the enemies before breaking.
        Activate it with the up key or W.""",
            40, (0, 0, 0), 550, 250)

        # Make the Ability "strong bullet"
        self.strong_bullet_square = AbilityButton(self, "B", 130)
        self.warp_square = AbilityButton(self, "S", 230)

        # Create a pygame clock
        self.clock = pygame.time.Clock()
        self.fps_meter = Text(self, f"FPS: {self.stats.current_fps}", 30, (0, 255, 0), 
            65, self.settings.screen_height - 30)

        # Start Alien Invasion in an inactive state.
        self.stats.game_layer = GS.MAINMENU

        self.alien_pattern = AP.THREEROWS
        # Important for new_level final frames
        self.random_flag = 0

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_fps()
            if self.stats.game_layer == GS.PLAYSCREEN:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_alien_bullets()
                self.strong_bullet_square._cooldown()
                self.warp_square._cooldown()
            self._update_screen()

    def _start_game(self):
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_layer = GS.PLAYSCREEN
        self.settings.initialize_dynamic_settings()
        self.warp_square._reset_cooldown()
        self.strong_bullet_square._reset_cooldown()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        for group in self.three_columns_group:
            group.empty()
        self.alien_bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()  

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)  

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                high_score = open("Games/Alien_Invasion/high_score.txt", "w")
                high_score.write(str(self.stats.high_score))
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_main_buttons(mouse_pos)
                self._check_pause_buttons(mouse_pos)
                
    def _check_main_buttons(self, mouse_pos):
        """Check the main screen buttons"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if self.stats.game_layer == GS.MAINMENU:
            if button_clicked:
            # Reset the game settings.
                self._start_game()
            elif self.info.rect.collidepoint(mouse_pos):
            # Go to info screen
                self.stats.game_layer = GS.INFOSCREEN

    def _check_pause_buttons(self, mouse_pos):
        """Check pause screen buttons"""
        if self.stats.game_layer == GS.PAUSEMENU:
            if self.main_menu.rect.collidepoint(mouse_pos):
                # Return to the main menu if clicked
                self.stats.game_layer = GS.MAINMENU
            elif self.resume.rect.collidepoint(mouse_pos):
                # Return to the game if clicked
                self.stats.game_layer = GS.PLAYSCREEN

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.stats.game_layer == GS.MAINMENU:
                self._start_game()
            elif self.stats.game_layer == GS.PLAYSCREEN:
                self._fire_bullet()
        elif event.key == pygame.K_p:
            if self.stats.game_layer == GS.MAINMENU:
                self._start_game()
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            if self.settings.normal_bullet and self.strong_bullet_square.cooldown_up:
                self.settings.strong_bullet()
                self.strong_bullet_square.covering = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            if not self.settings.warp_up and self.warp_square.cooldown_up:
                self.settings.warp_up = True
                self.warp_square.covering = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            self._check_escape_events()

    def _check_escape_events(self):
        """Change screens when q is pressed"""
        if self.stats.game_layer == GS.PLAYSCREEN:
            # Go to pause screen if on game screen
            self.stats.game_layer = GS.PAUSEMENU
            pygame.mouse.set_visible(True)
        elif self.stats.game_layer == GS.PAUSEMENU:
            # If on pause, go to the main menu
            high_score = open("Games/Alien_Invasion/high_score.txt", "w")
            high_score.write(str(self.stats.high_score))
            self.stats.game_layer = GS.MAINMENU
            pygame.mouse.set_visible(True)
        elif self.stats.game_layer == GS.INFOSCREEN:
            # Go back to the main menu
            self.stats.game_layer = GS.MAINMENU
        else:
            # Quit if on the main menu
            high_score = open("Games/Alien_Invasion/high_score.txt", "w")
            high_score.write(str(self.stats.high_score))
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _update_fps(self):
        """Update clock, then update fps and visual every 100 frames"""
        self.clock.tick(100)
        self.stats.tick_update += 1
        if self.stats.tick_update >= 100:
            self.stats.current_fps = self.clock.get_fps()
            self.stats.tick_update = 0
            self.fps_meter._prep_text(f"FPS: {round(self.stats.current_fps)}")

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
        self._check_alien_bullet_shield_collisions()

    def _update_alien_bullets(self):
        """Update alien bullets and get rid of out of bounds ones."""
        # Update their position
        self.alien_bullets.update()

        # If out of bounds, delete the bullet
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height - 20:
                self.alien_bullets.remove(bullet)

    def _strong_bullet_timer(self):
        """Tracks strong bullet usage, resets once it passes threshold"""
        if not self.settings.normal_bullet:
            self.settings.strong_bullets_fired += 1
            # Checks number of strong bullets, discontinues if necessary
            if self.settings.strong_bullets_fired > self.settings.strong_bullets_allowed:
                self.settings.normal_bullet_reset()
                self.strong_bullet_square.cooldown_start = True

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        self.collision_shell = []
        if self.alien_pattern == AP.BASIC:
            self.collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, self.settings.normal_bullet, True)
            self.collision_shell.append(self.collisions)
        # Have to check collisions for each group separately unfortunately
        elif self.alien_pattern == AP.THREEROWS:
            for index in range(len(self.three_columns_group)):
                self.collisions = pygame.sprite.groupcollide(
                    self.bullets, self.three_columns_group[index], self.settings.normal_bullet, True)
                self.collision_shell.append(self.collisions)
        for collision in self.collision_shell:
            for aliens in collision.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        # Random flag serves to have the half second sleep between levels
        # occur after the final alien has been deleted,
        # for aesthetic purposes
        if self.alien_pattern == AP.BASIC:
            if self.random_flag == 1:
                self.random_flag = 0
                self._new_level()
            if not self.aliens:
                self.random_flag = 1
        elif self.alien_pattern == AP.THREEROWS:
            # Weird backwards thinking, but simpler logic is checking
            # If any of them exist, and doing an else if that's not true
            if self.column3_aliens or self.column2_aliens or self.column1_aliens:
                pass
            elif self.random_flag == 1:
                self._new_level()
                self.random_flag = 0
            else:
                self.random_flag = 1
            
    def _check_alien_bullet_shield_collisions(self):
        """Respond to shield-shooter alien collisions."""
        if (pygame.sprite.spritecollide(self.warp_shield, self.alien_bullets, self.settings.warp_up)
            and self.settings.warp_up):
            self.settings.shield_hits += 1
            # If the shield has been hit too many times, start cooldown + it's broken
            if self.settings.shield_hits >= self.settings.allowed_hits:
                self.settings.shield_hits = 0
                self.warp_square.cooldown_start = True
                self.settings.warp_up = False

    def _new_level(self):
        """ Destroy existing bullets and create new fleet. """
        sleep(0.5)
        self.bullets.empty()
        self.alien_bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()
        self.strong_bullet_square._reset_cooldown()
        self.warp_square._reset_cooldown()
        self.settings.warp_up = False

        # Reset speeds sometimes
        if random.randint(1, 2) == 2:
            self.settings.column_direction_list[0] = 1
            self.settings.column_direction_list[1] = -1
            self.settings.column_direction_list[2] = 1

        # Increase level
        self.stats.level += 1
        self.sb.prep_level()

        # Stop strong bullet if active
        if not self.settings.normal_bullet:
            self.settings.normal_bullet_reset() 

    def _ship_hit(self):
        """Respond to the ship being hit by alien"""
        if self.stats.ships_left > 0:
            # Decrement ships left, and update graphics.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            for group in self.three_columns_group:
                group.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            # Reset directions
            self.settings.column_direction_list[0] = 1
            self.settings.column_direction_list[1] = -1   
            self.settings.column_direction_list[2] = 1

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Reset strong bullet
            if not self.settings.normal_bullet:
                self.settings.normal_bullet_reset()
            self.strong_bullet_square._reset_cooldown()
            # Reset shield things
            self.warp_square._reset_cooldown()
            # How/Why would it still be up idk, but in case
            self.settings.warp_up = False

            # Slow it down marginally
            self.settings.ship_speed *= 0.95
            self.settings.alien_speed *= 0.95
            self.settings.bullet_speed *= 0.95

            # Pause.
            sleep(1)
        else:
            self.stats.game_layer = GS.MAINMENU
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """
        Check if the fleet is at an edge, 
          then update the positions of all aliens in the fleet.
        """
        if self.alien_pattern == AP.BASIC:
            self.aliens.update()
            # Look for alien-ship collisions.
            if pygame.sprite.spritecollideany(self.ship, self.aliens):
                self._ship_hit()
        elif self.alien_pattern == AP.THREEROWS:
            for group in self.three_columns_group:
                group.update()
                if pygame.sprite.spritecollideany(self.ship, group):
                    self._ship_hit()
        # Hopefully having these after will prevent odd fleet down movement
        self._check_fleet_edges()
        self._check_aliens_bottom()
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit()

        # Fire the shooter aliens if needed.
        self._fire_shooter_aliens()
        
    def _fire_shooter_aliens(self):
        """Have one alien shoot at any one time, earlier list address favored"""
        # Runs through every shooter alien address
        if self.alien_pattern == AP.BASIC:
            for x in self.shooter_alien_addresses:
                # Checks number of bullets, that there is no one in front,
                # and checks that the alien is alive.
                if (len(self.alien_bullets) <= self.settings.alien_bullets_allowed
                    and self._check_in_front(x, self.aliens) and self.alien_start_list[x] in self.aliens
                    and self.time_since_shot >= 50):
                    self.time_since_shot = 0
                    new_bullet = AlienBullet(self, self.alien_start_list[x])
                    self.alien_bullets.add(new_bullet)
        elif self.alien_pattern == AP.THREEROWS:
            # Basically the same setup as before, just with optimized if statements
            # and accounting for checking through several groups
            # If using rows instead of columns, this will not work
            if (len(self.alien_bullets) <= self.settings.alien_bullets_allowed):
                for address in self.shooter_alien_addresses:
                    for group in self.three_columns_group:
                        if (self._check_in_front(address, group) and 
                        self.alien_start_list[address] in group) and self.time_since_shot >= 50:
                            self.time_since_shot = 0
                            new_bullet = AlienBullet(self, self.alien_start_list[address])
                            self.alien_bullets.add(new_bullet)
        self.time_since_shot += 1

    def _check_in_front(self, alien, group):
        """Check before firing that no aliens in specified group are in front of the shooter"""
        if alien > 26: 
            return True
        elif alien // 9 == 2 and (self.alien_start_list[alien + 9] in group):
            return False
        elif alien // 9 == 1:
            for x in range(1, 3):
                if self.alien_start_list[alien + 9 * x] in group:
                    return False
        elif alien < 9:
            for x in range(1, 4):
                if self.alien_start_list[alien + 9 * x] in group:
                    return False
        return True

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Make an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        self.number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                    (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the list of potential shooter aliens/addresses
        self.shooter_alien_addresses = []
        self.time_since_shot = 0

        # Created here so each new alien in this mode can be appended
        self.alien_start_list = []

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(self.number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create a alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        # 1 in 3 aliens are a shooter alien
        if random.randint(1, 3) == 3:
            self.shooter_alien_addresses.append(alien_number + row_number * 9)
        if self.alien_pattern == AP.BASIC:
            self.aliens.add(alien)
        elif self.alien_pattern == AP.THREEROWS:
            if alien_number < 3:
                self.column1_aliens.add(alien)
                #print(f"1: {alien_number + row_number * 9}")
            elif alien_number < 6:
                self.column2_aliens.add(alien)
                #print(f"2: {alien_number + row_number * 9}")
            else:
                self.column3_aliens.add(alien)
                #print(f"3: {alien_number + row_number * 9}")
        
        self.alien_start_list.append(alien)

    def _check_fleet_edges(self):
        """Respond if an aliens have reached an edge."""
        if self.alien_pattern == AP.BASIC:
            for alien in self.aliens.sprites():
                if alien.check_edges() == CSS.ONEGROUP:
                    self._change_fleet_direction()
                    break
        elif self.alien_pattern == AP.THREEROWS:
            for row_group in self.three_columns_group:
                for alien in row_group:
                    if alien.check_edges() == CSS.FIRSTCOLUMN:
                        self.settings.column_direction_list[0] *= -1
                        self._drop_alien_group(self.column1_aliens)
                    elif alien.check_edges() == CSS.SECONDCOLUMN:
                        self.settings.column_direction_list[1] *= -1
                        self._drop_alien_group(self.column2_aliens)
                    elif alien.check_edges() == CSS.THIRDCOLUMN:
                        self.settings.column_direction_list[2] *= -1
                        self._drop_alien_group(self.column3_aliens)
                    elif alien.check_edges() == CSS.FIRSTTWO:
                        for blank in CSS.FIRSTTWO._value_:
                            self.settings.column_direction_list[blank] *= -1
                            self._drop_alien_group(self.three_columns_group[blank])
                    elif alien.check_edges() == CSS.LASTTWO:
                        for blank in CSS.LASTTWO._value_:
                            self.settings.column_direction_list[blank] *= -1
                            self._drop_alien_group(self.three_columns_group[blank])
                    elif alien.check_edges() == CSS.ENDTWO:
                        for blank in CSS.ENDTWO._value_:
                            self.settings.column_direction_list[blank] *= -1
                            self._drop_alien_group(self.three_columns_group[blank])

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        if self.alien_pattern == AP.BASIC:
            for alien in self.aliens.sprites():
                if alien.rect.bottom >= screen_rect.bottom:
                    # Treat it as if a ship got hit.
                    self._ship_hit()
                    break
        elif self.alien_pattern == AP.THREEROWS:
            for group in self.three_columns_group:
                for alien in group:
                    if alien.rect.bottom >= screen_rect.bottom:
                        self._ship_hit()
                        break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        if self.alien_pattern == AP.BASIC:
            self.settings.fleet_direction *= -1
            for alien in self.aliens.sprites():
                alien.rect.y += self.settings.fleet_drop_speed

    def _drop_alien_group(self, group):
        for alien in group:
            alien.rect.y += self.settings.group_drop_speed        

    def _update_play_screen(self):
        """Draw everything on the play screen"""
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_alien_bullet()
        if self.alien_pattern == AP.BASIC:
            self.aliens.draw(self.screen)
        elif self.alien_pattern == AP.THREEROWS:
            self.column1_aliens.draw(self.screen)
            self.column2_aliens.draw(self.screen)
            self.column3_aliens.draw(self.screen)

        # Draw the score info and ability squares
        self.sb.show_score()
        self.strong_bullet_square.draw_ability_square()
        self.warp_square.draw_ability_square()
        self.warp_shield.draw_shield()
        
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        # Draw the play screen when appropriate
        if self.stats.game_layer == GS.PLAYSCREEN:
            self._update_play_screen()
            
        # Draw the main menu when appropriate.
        elif self.stats.game_layer == GS.MAINMENU:
            self.title.draw_text()
            self.play_button.draw_button()
            self.info.draw_button()
            
        # Draw the pause screen when appropriate
        elif self.stats.game_layer == GS.PAUSEMENU:
            self.pause.draw_text()
            self.main_menu.draw_button()
            self.resume.draw_button()

        # Draw the information screen when appropriate
        elif self.stats.game_layer == GS.INFOSCREEN:
            self.strong_bullet_info.draw_text()
            self.shield_info.draw_text()

        # Draw the fps screen on every screen
        self.fps_meter.draw_text()
        
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
