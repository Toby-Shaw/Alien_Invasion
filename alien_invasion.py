from ast import Pass
from pickle import TRUE
import sys
from time import sleep
import random
import os

import pygame

from Play_Screen.settings import Settings
from Play_Screen.ship import Ship
from Play_Screen.bullet import Bullet
from UI.game_stats import Gamestats
from UI.button import Button
from Play_Screen.scoreboard import Scoreboard
from Play_Screen.ability_square import AbilityButton
from UI.text import Text
from Play_Screen.shield import WarpShield
from UI.all_enums import GameStates as GS
from UI.all_enums import AlienPattern as AP
from Play_Screen.horde import Horde
from game_sounds import GameSounds
from UI.slider import Slider
from Play_Screen.boss import Boss
from UI.all_enums import BossPattern as BP
from UI.key_checker import *

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.mixer.init()
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics,
        # and make a scoreboard
        self.stats = Gamestats(self)
        self.sb = Scoreboard(self)
        self.alien_pattern = AP.THREEROWS

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.horde = Horde(self)
        # Create the warp shield
        self.warp_shield = WarpShield(self)

        # Make the Play button and other buttons
        self.play_button = Button(self, "Play", (0, 255, 0),
            (self.settings.screen_width / 2), (self.settings.screen_height / 2 - 50))
        self.main_menu = Button(self, "Main Menu", (0, 255, 0), 
            (self.settings.screen_width / 2), self.settings.screen_height / 2 + 100)
        self.resume = Button(self, "Resume", (0, 255, 0),
            (self.settings.screen_width / 2), (self.settings.screen_height / 2))
        self.info = Button(self, "Information", (0, 255, 0), 
            self.settings.screen_width / 2, (self.settings.screen_height / 2 + 50))
        self.settings_button = Button(self, "Settings", (0, 255, 0),
            self.settings.screen_width / 2, (self.settings.screen_height / 2 + 150))
        self.highscores_button = Button(self, "Highscores", (0, 255, 0), 
            self.settings.screen_width / 2, self.settings.screen_height / 2 + 250)

        # Make the title + Pause text
        self.title = Text(self, "Alien Invasion", 110, (0, 255, 0), 
            (self.settings.screen_width / 2), 180)
        self.title_switch = 0
        self.pause = Text(self, "Paused", 110, (0, 255, 0),
            (self.settings.screen_width / 2), 180)
        self.game_over = Text(self, "Game Over", 170, (0, 255, 0),
            (self.settings.screen_width / 2), 270)

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
        self.music_text = Text(self, """Music Volume:              Sound Volume:""",
                    60, (0, 0, 0), 300, 200)
        self.music_slider = Slider(self, (150, 255, 150), 750, 200, 0)
        self.sound_slider = Slider(self, (150, 255, 150), 750, 480, 1)

        # Make the Ability "strong bullet"
        self.strong_bullet_square = AbilityButton(self, "B", 130)
        self.warp_square = AbilityButton(self, "S", 230)

        # Create a pygame clock
        self.clock = pygame.time.Clock()
        self.fps_meter = Text(self, f"FPS: {self.stats.current_fps}", 30, (0, 255, 0), 
            65, self.settings.screen_height - 30)

        # Start Alien Invasion in an inactive state.
        self.stats.game_layer = GS.MAINMENU
        self.cheats = True
        self.various_alien_bullet_groups = [self.horde.alien_bullets, self.horde.boss.alien_bullets]
        self.general_play = True
        # Music
        self.game_sounds = GameSounds()
        # Important for new_level final frames
        self.random_flag = 0

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_fps()
            if self.stats.game_layer == GS.PLAYSCREEN:
                if self.general_play:
                    self.ship.update()
                    self.horde._update_aliens()
                    self._update_bullets()
                    self.horde._update_alien_bullets()
                    self.strong_bullet_square._cooldown()
                    self.warp_square._cooldown()
                else:
                    self.horde.boss.check_cut_scene_movement()
            elif self.stats.game_layer == GS.SETTINGS:
                # update the sliders each frame if necessary
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                check_slider(self, mouse_pos, mouse_pressed[0], False)
            elif self.stats.game_layer == GS.MAINMENU:
                self._update_title()
            self._update_screen()

    def _start_game(self):
        # Reset the game statistics.
        self.stats.reset_stats()
        self.settings.initialize_dynamic_settings()
        self.strong_bullet_square = AbilityButton(self, "B", 130)
        self.warp_square = AbilityButton(self, "S", 230)
        self.warp_square._reset_cooldown()
        self.strong_bullet_square._reset_cooldown()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.game_sounds.sound_channel.play(self.game_sounds.start_sound)
        self.alien_pattern = AP.THREEROWS

        # Get rid of any remaining aliens and bullets.
        self.horde.aliens.empty()
        self.horde.boss.alien_bullets.empty()
        self.bullets.empty()
        for group in self.horde.three_columns_group:
            group.empty()
        self.horde.alien_bullets.empty()
        self.horde.boss_shell.empty()

        # Create a new fleet and center the ship.
        self.horde.alien_pattern = self.alien_pattern
        self.horde._create_fleet()
        self.ship.center_ship()  

        # Hide the mouse cursor.
        sleep(0.4)
        pygame.mouse.set_visible(False)  
        self.stats.game_layer = GS.PLAYSCREEN

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                high_score = open("Games/Alien_Invasion/high_score.txt", "w")
                high_score.write(str(self.stats.high_score))
                sys.exit()
            elif event.type == pygame.KEYUP:
                check_keyup_events(self, event)
            if self.general_play:
                if event.type == pygame.KEYDOWN:
                    check_keydown_events(self, event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    check_main_buttons(self, mouse_pos)
                    check_pause_buttons(self, mouse_pos)
                    check_over_buttons(self, mouse_pos)
                    check_slider(self, mouse_pos, True, True)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.music_slider.clicked = False
                    self.sound_slider.clicked = False

    def _update_fps(self):
        """Update clock, then update fps and visual every 100 frames"""
        self.clock.tick(100)
        self.stats.tick_update += 1
        if self.stats.tick_update >= 100:
            self.stats.current_fps = self.clock.get_fps()
            self.stats.tick_update = 0
            self.fps_meter._prep_text(f"FPS: {round(self.stats.current_fps)}")

    def _update_title(self):
        """Update the title animation"""
        if self.title_switch > 100:
            self.title_switch = 0
            if self.title.font_color == (0, 255, 0):
                self.title.font_color = (255, 255, 255)
                self.title.bg_color = (0, 255, 0)
            else:
                self.title.font_color = (0, 255, 0)
                self.title.bg_color = self.settings.bg_color
            self.title._prep_text("Alien Invasion")
        self.title_switch += 1

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
            self.bullets, self.horde.aliens, self.settings.normal_bullet, True)
            self.collision_shell.append(self.collisions)
        elif self.alien_pattern == AP.THREEROWS:
            for index in range(len(self.horde.three_columns_group)):
                self.collisions = pygame.sprite.groupcollide(
                    self.bullets, self.horde.three_columns_group[index], self.settings.normal_bullet, True)
                self.collision_shell.append(self.collisions)
        elif self.alien_pattern == AP.BOSSROOM:
            self.collisions = pygame.sprite.spritecollide(self.horde.boss, self.bullets, True)
            if self.collisions:
                if not self.settings.normal_bullet:
                    if self.horde.boss.health >= 15: self.horde.boss.health -= 15
                    elif self.horde.boss.health < 15: self.horde.boss.health = 0
                    self.horde.boss.healthbar._update_health()
                else:
                    if self.horde.boss.health >= 7: self.horde.boss.health -= 7 
                    elif self.horde.boss.health < 7: self.horde.boss.health = 0
                    self.horde.boss.healthbar._update_health()
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
            if not self.horde.aliens:
                self.random_flag = 1
        elif self.alien_pattern == AP.THREEROWS:
            # if any exist, don't do anything, otherwise new level
            if self.horde.column3_aliens or self.horde.column2_aliens or self.horde.column1_aliens:
                pass
            elif self.random_flag == 1:
                self._new_level()
                self.random_flag = 0
            elif self.random_flag == 0:
                self.random_flag = 1
        elif self.alien_pattern == AP.BOSSROOM:
            if self.horde.boss.health == 0:
                self.alien_pattern = AP.THREEROWS
                self.stats.score += 100000
                self.sb.prep_score()
                self.sb.check_high_score()
            
    def _check_alien_bullet_shield_collisions(self):
        """Respond to shield-shooter alien collisions."""
        # Finagled a way to get all groups to work regardless of pattern
        # By doing odd alien_pattern thing, will make more flexible later
        if (pygame.sprite.spritecollide(self.warp_shield, 
            self.various_alien_bullet_groups[self.alien_pattern._value_ // 2], self.settings.warp_up)
            and self.settings.warp_up):
                self._shield_hit()
    
    def _shield_hit(self, hits = 1):
        """Shield has been hit, act accordingly"""
        self.game_sounds.sound_channel.play(self.game_sounds.shield_hit)
        self.settings.shield_hits += hits
        # If the shield has been hit too many times, start cooldown + it's broken
        if self.settings.shield_hits >= self.settings.allowed_hits:
            self.settings.shield_hits = 0
            self.warp_square.cooldown_start = True
            self.settings.warp_up = False

    def _new_level(self):
        """ Destroy existing bullets and create new fleet. """
        sleep(0.5)
        self.bullets.empty()
        self.horde.alien_bullets.empty()
        self.horde.boss.alien_bullets.empty()
        # Increase level
        self.stats.level += 1
        self.sb.prep_level()
        if self.stats.level % 5 == 0:
            self.warp_square = AbilityButton(self, "S", 50)
            self.strong_bullet_square = AbilityButton(self, "B", -50)
            self.horde.boss = Boss(self.horde)
            self.horde.boss_shell.add(self.horde.boss)
            self.various_alien_bullet_groups = [self.horde.alien_bullets, 
                            self.horde.boss.alien_bullets]
            self.alien_pattern = AP.BOSSROOM
            self.ship.center_ship()
            self.horde.boss.cut_scene()
        elif self.stats.level % 5 == 1 and self.stats.level != 1:
            self.warp_square = AbilityButton(self, "S", 170)
            self.strong_bullet_square = AbilityButton(self, "B", 70)
            self.game_sounds.change_back()
        if self.alien_pattern == AP.THREEROWS or self.alien_pattern == AP.BASIC:
            self.horde._create_fleet()
            self.settings.increase_speed()
            # Reset speeds sometimes
            if random.randint(1, 2) == 2:
                self.settings.column_direction_list[0] = 1
                self.settings.column_direction_list[1] = -1
                self.settings.column_direction_list[2] = 1
        self.strong_bullet_square._reset_cooldown()
        self.warp_square._reset_cooldown()
        self.settings.warp_up = False
        # Stop strong bullet if active
        if not self.settings.normal_bullet:
            self.settings.normal_bullet_reset() 

    def _ship_hit(self):
        """Respond to the ship being hit by alien"""
        self.game_sounds.sound_channel.play(self.game_sounds.ship_hit)
        if self.stats.ships_left > 0:
            # Decrement ships left, and update graphics.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.horde.aliens.empty()
            for group in self.horde.three_columns_group:
                group.empty()
            self.bullets.empty()
            self.horde.boss.alien_bullets.empty()
            self.horde.boss_shell.empty()
            self.horde.alien_bullets.empty()

            # Reset directions
            self.settings.column_direction_list[0] = 1
            self.settings.column_direction_list[1] = -1   
            self.settings.column_direction_list[2] = 1

            # Reset strong bullet
            self.settings.normal_bullet_reset()
            self.strong_bullet_square._reset_cooldown()
            # Reset shield things
            self.warp_square._reset_cooldown()
            self.settings.warp_up = False

            # Slow it down marginally
            self.settings.ship_speed *= 0.95
            self.settings.alien_speed *= 0.95
            self.settings.bullet_speed *= 0.95

            # Create a new fleet and center the ship.
            if self.alien_pattern == AP.BASIC or self.alien_pattern == AP.THREEROWS:
                self.horde._create_fleet()
                self.ship.center_ship()
                sleep(1)
            elif self.alien_pattern == AP.BOSSROOM:
                temp_health = self.horde.boss.health
                temp_coords = self.horde.boss.rect.center
                temp_pattern = self.horde.boss.boss_pattern
                temp_directions = [self.horde.boss.xdirection, self.horde.boss.ydirection]
                self.horde.boss = Boss(self.horde, health=temp_health, coords=temp_coords, directions=temp_directions)
                self.horde.boss_shell.add(self.horde.boss)
                self.various_alien_bullet_groups = [self.horde.alien_bullets, 
                            self.horde.boss.alien_bullets]
                self.horde.boss.boss_pattern = temp_pattern
                self.horde.boss.healthbar._update_health()
                sleep(1) 
        else:
            self.stats.game_layer = GS.ENDSCREEN
            self.alien_pattern = AP.THREEROWS
            pygame.mouse.set_visible(True)

    def _update_play_screen(self):
        """Draw everything on the play screen"""
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien_bullet in self.horde.alien_bullets.sprites():
            alien_bullet.draw_alien_bullet()
        for alien_bullet in self.horde.boss.alien_bullets.sprites():
            alien_bullet.draw_alien_bullet()
        if self.alien_pattern == AP.BASIC:
            self.horde.aliens.draw(self.screen)
        elif self.alien_pattern == AP.THREEROWS:
            for group in self.horde.three_columns_group:
                group.draw(self.screen)
        elif self.alien_pattern == AP.BOSSROOM:
            self.horde.boss.draw()

        # Draw the score info and ability squares
        if not self.alien_pattern == AP.BOSSROOM:
            self.sb.show_score()
        else:
            if self.general_play:
                self.horde.boss.healthbar._prep_name()
                self.horde.boss.healthbar._draw_health_bar()
            self.sb.show_ships()
        self.strong_bullet_square.draw_ability_square()
        self.warp_square.draw_ability_square()
        self.warp_shield.draw_shield()

    def _update_main_menu(self):
        """Draw the main screen, including alien shape and buttons"""
        if self.title.font_color != (0, 255, 0):
            self.light_green = (175, 255, 175)
            pygame.draw.line(self.screen, (0, 255, 0), (450, 200), (250, 800), width = 10)
            pygame.draw.line(self.screen, (0, 255, 0), (self.settings.screen_width - 450, 200), (self.settings.screen_width - 250, 800), width = 10)
            for x in range(31):
                if x <= 15:
                    pygame.draw.line(self.screen, self.light_green, ((450 + (x + 1) * 10), 200), ((250 + (x + 1) * 10), 800), width = 10)
                    pygame.draw.line(self.screen, self.light_green, ((self.settings.screen_width - 450 - (x + 15) * 10), 200), 
                            ((self.settings.screen_width - 250 - (x + 15) * 10), 800), width = 10)
                    pygame.draw.line(self.screen, self.light_green, (self.settings.screen_width / 2 - 3 * x, 200), 
                            (self.settings.screen_width / 2 - 2 * x, 800),  width = 10)
                else:
                    pygame.draw.line(self.screen, self.light_green, ((450 + (x + 1) * 10), 200), ((250 + (x + 1) * 10), 800), width = 10)
                    pygame.draw.line(self.screen, self.light_green, ((self.settings.screen_width - 450 - (x - 15) * 10), 200), 
                            ((self.settings.screen_width - 250 - (x - 15) * 10), 800), width = 10)
                    pygame.draw.line(self.screen, self.light_green, (self.settings.screen_width / 2 + 2 * (x - 15), 200),
                            (self.settings.screen_width / 2 + 3 * (x - 15), 800),  width = 10) 
            pygame.draw.ellipse(self.screen, (0, 255, 0), (150, self.title.text_rect_list[0].top - 50, self.settings.screen_width - 300, 
                self.title.text_rect_list[0].bottom - 50))
        self.title.draw_text()
        self.play_button.draw_button()
        self.info.draw_button()
        self.settings_button.draw_button()
        self.highscores_button.draw_button()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        # Draw the play screen when appropriate
        if self.stats.game_layer == GS.PLAYSCREEN:
            self._update_play_screen()
        # Draw the main menu when appropriate.
        elif self.stats.game_layer == GS.MAINMENU:
            self._update_main_menu()
        # Draw the pause screen when appropriate
        elif self.stats.game_layer == GS.PAUSEMENU:
            self.pause.draw_text()
            self.main_menu.draw_button()
            self.resume.draw_button()
            self.settings_button.draw_button()

        # Draw the information screen when appropriate
        elif self.stats.game_layer == GS.INFOSCREEN:
            self.strong_bullet_info.draw_text()
            self.shield_info.draw_text()

        elif self.stats.game_layer == GS.ENDSCREEN:
            self.main_menu.draw_button()
            self.game_over.draw_text()

        elif self.stats.game_layer == GS.SETTINGS:
            self.music_text.draw_text()
            self.music_slider._draw_slider()
            self.sound_slider._draw_slider()

        elif self.stats.game_layer == GS.HIGHSCORES:
            self.sb.show_high_scores()

        # Draw the fps screen on every screen
        self.fps_meter.draw_text()
        
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
