import pygame
import sys
from UI.all_enums import GameStates as GS
from UI.all_enums import AlienPattern as AP

"""This includes all of the basic key checker methods that I'm not messing with since they work well,
    and don't need to be in the main file"""
def check_main_buttons(self, mouse_pos):
    """Check the main screen buttons"""
    button_clicked = self.play_button.rect.collidepoint(mouse_pos)
    if self.stats.game_layer == GS.MAINMENU:
        if button_clicked:
        # Reset the game settings.
            self._start_game()
        elif self.info.rect.collidepoint(mouse_pos):
        # Go to info screen
            self.stats.game_layer = GS.INFOSCREEN
        elif self.settings_button.rect.collidepoint(mouse_pos):
            self.previous_layer = GS.MAINMENU
            self.stats.game_layer = GS.SETTINGS
        elif self.highscores_button.rect.collidepoint(mouse_pos):
            self.stats.game_layer = GS.HIGHSCORES

def check_pause_buttons(self, mouse_pos):
    """Check pause screen buttons"""
    if self.stats.game_layer == GS.PAUSEMENU:
        if self.main_menu.rect.collidepoint(mouse_pos):
            # Return to the main menu if clicked
            if self.alien_pattern == AP.BOSSROOM:
                self.game_sounds.change_back()
            self.stats.game_layer = GS.MAINMENU
            self.title_switch = 0
        elif self.resume.rect.collidepoint(mouse_pos):
            # Return to the game if clicked
            self.stats.game_layer = GS.PLAYSCREEN
            pygame.mouse.set_visible(False)
        elif self.settings_button.rect.collidepoint(mouse_pos):
            self.previous_layer = GS.PAUSEMENU
            self.stats.game_layer = GS.SETTINGS

def check_over_buttons(self, mouse_pos):
    """Check end screen buttons"""
    if self.stats.game_layer == GS.ENDSCREEN:
        if self.main_menu.rect.collidepoint(mouse_pos):
            self.title_switch = 0
            self.stats.game_layer = GS.MAINMENU

def check_slider(self, mouse_pos, mouse_pressed, new_click):
    """Check the settings sliders"""
    if self.stats.game_layer == GS.SETTINGS and mouse_pressed:
        self.music_slider.update(mouse_pos, new_click)
        self.sound_slider.update(mouse_pos, new_click)

def check_keydown_events(self, event):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        self.ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        self.ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if self.stats.game_layer == GS.MAINMENU:
            self._start_game()
        elif self.stats.game_layer == GS.PLAYSCREEN:
            self.game_sounds.sound_channel.play(self.game_sounds.bullet_fired, 0, 500)
            self._fire_bullet()
        elif self.stats.game_layer == GS.PAUSEMENU:
            self.stats.game_layer = GS.PLAYSCREEN
    elif event.key == pygame.K_p:
        if self.stats.game_layer == GS.MAINMENU:
            self._start_game()
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        if self.settings.normal_bullet and self.strong_bullet_square.cooldown_up and self.stats.game_layer == GS.PLAYSCREEN:
            self.game_sounds.sound_channel.play(self.game_sounds.strong_start, 0, 550)
            self.settings.strong_bullet()
            self.strong_bullet_square.covering = True
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        if not self.settings.warp_up and self.warp_square.cooldown_up and self.stats.game_layer == GS.PLAYSCREEN:
            self.game_sounds.sound_channel.play(self.game_sounds.shield_up)
            self.settings.warp_up = True
            self.warp_square.covering = True
    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        _check_escape_events(self)
    elif event.key == pygame.K_b and self.cheats == True:
        for group in self.horde.three_columns_group:
            group.empty()
    elif event.key == pygame.K_n and self.cheats == True:
        self.horde.boss.health -= 100
        self.horde.boss.healthbar._update_health()

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
        self.title_switch = 0
        if self.alien_pattern == AP.BOSSROOM:
            self.game_sounds.change_back()
        pygame.mouse.set_visible(True)
    elif self.stats.game_layer == GS.INFOSCREEN or self.stats.game_layer == GS.ENDSCREEN or self.stats.game_layer == GS.HIGHSCORES:
        # Go back to the main menu
        self.stats.game_layer = GS.MAINMENU
        self.title_switch = 0
        if self.alien_pattern == AP.BOSSROOM:
            self.game_sounds.change_back()
    elif self.stats.game_layer == GS.SETTINGS:
        self.stats.game_layer = self.previous_layer
    else:
        # Quit if on the main menu
        high_score = open("Games/Alien_Invasion/high_score.txt", "w")
        high_score.write(str(self.stats.high_score))
        sys.exit()

def check_keyup_events(self, event):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        self.ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        self.ship.moving_left = False