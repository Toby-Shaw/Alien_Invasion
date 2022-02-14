import pygame
from UI.all_enums import AlienPattern as AP
from UI.all_enums import BossPattern as BP
from Play_Screen.alien_bullet import AlienBullet
import time
import random

class Boss:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.base_image = pygame.image.load("Games/Alien_Invasion/Images/alien_big.png")
        #self.image = pygame.transform.scale2x(self.base_image)
        self.rect = self.base_image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.alien_bullets = pygame.sprite.Group()
        self.time_since_shot = 0
        self.previous_step = 0
        self.number_steps = 0
        self.basic_speed = 5
        # 1 = right, left = -1
        self.xdirection = 1
        self.ydirection = 1
        self.all_patterns = [BP.SHOOTBASIC, BP.DARTTOHIT]
        self.switch_cooldown = 0
        self.switch_time = False
        self.number_screen_hits = 0
    
    def draw(self):
        self.screen.blit(self.base_image, self.rect)

    def update(self, boss_pattern):
        if self.ai_game.alien_pattern == AP.BOSSROOM:
            self._shoot_bullet()
            self._move_accordingly(boss_pattern)
            self.alien_bullets.update()
            for bullet in self.alien_bullets.copy():
                if bullet.rect.top >= self.settings.screen_height - 35:
                    self.alien_bullets.remove(bullet)
            if self.switch_time:
                self._switch_pattern()
            self.switch_cooldown += 1

    def _switch_pattern(self):
        if self.switch_cooldown > 20 and random.randint(1, 3) == 3:
            self.switch_cooldown = 0
            self.switch_time = False
            self.ai_game.boss_pattern = random.choice(self.all_patterns)

    def _move_accordingly(self, pattern):
        if pattern == BP.SHOOTBASIC:
            self.x += 5 * self.xdirection
            self.rect.x = self.x
            if self._check_screen_edges():
                self.xdirection *= -1
                self.number_screen_hits += 1
            if self.number_screen_hits == 5:
                self.number_screen_hits = 0
                self.switch_time = True
        elif pattern == BP.DARTTOHIT:
            if self._check_screen_edges():
                self.ydirection *= -1
                self.number_screen_hits += 1
                self.y += 60 * self.ydirection
                self.x += 150 * self.xdirection
                self.rect.y = self.y
                self.rect.x = self.x
                if self._check_screen_edges():
                    self.xdirection *= -1
                    self.x += 50 * self.xdirection
                    self.rect.x = self.x
            else:
                self.y += 5 * self.ydirection
                self.rect.y = self.y
                if self.rect.y <= 300 and self.number_screen_hits == 4:
                    self.switch_time = True
                    self.number_screen_hits = 0
    
    def _check_screen_edges(self):
        if self.rect.left <= 0 or self.rect.right >= self.settings.screen_width:
            return True
        elif self.rect.bottom >= self.settings.screen_height or self.rect.top <= 0:
            return True

    def _shoot_bullet(self):
        if self.time_since_shot > 50:
            self.time_since_shot = 0
            new_bullet = AlienBullet(self.ai_game, self)
            self.alien_bullets.add(new_bullet)
        self.time_since_shot += 1
    
    def cut_scene(self):
        self.ai_game.general_play = False
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("Games/Alien_Invasion/Music/Running_scared.wav")
        pygame.mixer.music.play(-1)
        self.start_time = time.time()
        self.rect.bottom = 0
        self.rect.centerx = self.ai_game.settings.screen_width / 2
        self.check_cut_scene_movement()
        

    def check_cut_scene_movement(self):
        if time.time() - self.start_time > self.previous_step:
            if self.number_steps <= 3:
                self.previous_step += 0.82
                self.rect.y += 40
            elif self.number_steps <= 11:
                self.previous_step += 0.41
                self.rect.y += 20
            elif self.number_steps <= 15:
                self.previous_step += 0.205
                self.rect.y += 10
            self.number_steps += 1
        self.x = self.rect.x
        self.y = self.rect.y
        if time.time() - self.start_time >= 9.6:
            self.ai_game.general_play = True
        