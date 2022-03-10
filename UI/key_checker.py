import pygame
import sys
from UI.all_enums import GameStates as GS
from UI.all_enums import AlienPattern as AP

class Keychecker:
    def __init__(self, ai_game):
        self.ai = ai_game

    def check_main_buttons(self, mouse_pos):
        """Check the main screen buttons"""
        button_clicked = self.ai.play_button.rect.collidepoint(mouse_pos)
        if self.ai.stats.game_layer == GS.MAINMENU:
            if button_clicked:
            # Reset the game settings.
                self.ai._start_game()
            elif self.ai.info.rect.collidepoint(mouse_pos):
            # Go to info screen
                self.ai.stats.game_layer = GS.INFOSCREEN
            elif self.ai.main_settings_button.rect.collidepoint(mouse_pos):
                self.previous_layer = GS.MAINMENU
                self.ai.stats.game_layer = GS.SETTINGS
            elif self.ai.highscores_button.rect.collidepoint(mouse_pos):
                self.ai.sb.prep_high_scores()
                self.ai.stats.game_layer = GS.HIGHSCORES

    def check_pause_buttons(self, mouse_pos):
        """Check pause screen buttons"""
        if self.ai.stats.game_layer == GS.PAUSEMENU:
            if self.ai.main_menu.rect.collidepoint(mouse_pos):
                # Return to the main menu if clicked
                self._check_high_score_before_main()
                if self.ai.alien_pattern == AP.BOSSROOM:
                    self.ai.game_sounds.change_back()
                self.ai.title_switch = 0
            elif self.ai.resume.rect.collidepoint(mouse_pos):
                # Return to the game if clicked
                self.ai.stats.game_layer = GS.PLAYSCREEN
                pygame.mouse.set_visible(False)
            elif self.ai.pause_settings_button.rect.collidepoint(mouse_pos):
                self.previous_layer = GS.PAUSEMENU
                self.ai.stats.game_layer = GS.SETTINGS

    def check_over_buttons(self, mouse_pos):
        """Check end screen buttons"""
        if self.ai.stats.game_layer == GS.ENDSCREEN:
            if self.ai.main_menu.rect.collidepoint(mouse_pos):
                self.ai.title_switch = 0
                self.ai.game_sounds.change_back()
                self._check_high_score_before_main()

    def check_slider(self, mouse_pos, mouse_pressed, new_click):
        """Check the settings sliders"""
        if self.ai.stats.game_layer == GS.SETTINGS and mouse_pressed:
            self.ai.music_slider.update(mouse_pos, new_click)
            self.ai.sound_slider.update(mouse_pos, new_click)

    def check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ai.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ai.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.ai.stats.game_layer == GS.MAINMENU:
                self.ai._start_game()
            elif self.ai.stats.game_layer == GS.PLAYSCREEN:
                self.ai.game_sounds.sound_channel.play(self.ai.game_sounds.bullet_fired, 0, 500)
                self.ai._fire_bullet()
            elif self.ai.stats.game_layer == GS.PAUSEMENU:
                self.ai.stats.game_layer = GS.PLAYSCREEN
        elif event.key == pygame.K_p:
            if self.ai.stats.game_layer == GS.MAINMENU:
                self.ai._start_game()
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            if self.ai.settings.normal_bullet and self.ai.strong_bullet_square.cooldown_up and self.ai.stats.game_layer == GS.PLAYSCREEN:
                self.ai.game_sounds.sound_channel.play(self.ai.game_sounds.strong_start, 0, 550)
                self.ai.settings.strong_bullet()
                self.ai.strong_bullet_square.covering = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            if not self.ai.settings.warp_up and self.ai.warp_square.cooldown_up and self.ai.stats.game_layer == GS.PLAYSCREEN:
                self.ai.game_sounds.sound_channel.play(self.ai.game_sounds.shield_up)
                self.ai.settings.warp_up = True
                self.ai.warp_square.covering = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            self._check_escape_events()
        elif event.key == pygame.K_b and self.ai.cheats == True:
            for group in self.ai.horde.three_columns_group:
                group.empty()
        elif event.key == pygame.K_n and self.ai.cheats == True:
            self.ai.horde.boss.health -= 100
            self.ai.horde.boss.healthbar._update_health()

    def _check_escape_events(self):
        """Change screens when q is pressed"""
        if self.ai.stats.game_layer == GS.PLAYSCREEN:
            # Go to pause screen if on game screen
            self.ai.stats.game_layer = GS.PAUSEMENU
            pygame.mouse.set_visible(True)
        elif self.ai.stats.game_layer == GS.PAUSEMENU:
            # If on pause, go to the main menu
            self._check_high_score_before_main()
            self.ai.title_switch = 0
            if self.ai.alien_pattern == AP.BOSSROOM:
                self.ai.game_sounds.change_back()
            pygame.mouse.set_visible(True)
        elif self.ai.stats.game_layer == GS.INFOSCREEN or self.ai.stats.game_layer == GS.HIGHSCORES:
            # Go back to the main menu
            self.ai.stats.game_layer = GS.MAINMENU
            self.ai.title_switch = 0
        elif self.ai.stats.game_layer == GS.ENDSCREEN:
            self._check_high_score_before_main()
            self.ai.title_switch = 0
            if self.ai.alien_pattern == AP.BOSSROOM:
                self.ai.game_sounds.change_back()
        elif self.ai.stats.game_layer == GS.SETTINGS:
            self.ai.stats.game_layer = self.previous_layer
        else:
            # Quit if on the main menu
            self.ai.sb._update_high_scores_page()
            sys.exit()

    def check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ai.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ai.ship.moving_left = False

    def _check_high_score_before_main(self):
        if self.ai.stats.score > self.ai.stats.high_score[4]:
            self.ai.sb._update_high_scores_page()
        else: self.ai.stats.game_layer = GS.MAINMENU