import pygame
from UI.all_enums import AlienPattern as AP
from UI.all_enums import BossPattern as BP
from Play_Screen.alien_bullet import AlienBullet
import time
import random
from pygame.sprite import Sprite

class Boss(Sprite):
    def __init__(self, horde):
        """Initialize the Boss placement and things"""
        super().__init__()
        self.ai_game = horde
        self.screen = horde.screen
        self.settings = horde.settings
        self.horde = horde

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
        self.needed_screen_hits = random.randint(3, 6)
        self.delay_frames = random.randint(5, 100)
        self.delayed_frames = 0
    
    def draw(self):
        """Draw the boss"""
        self.screen.blit(self.base_image, self.rect)

    def update(self, boss_pattern):
        """If the alien_pattern is correct, shoot, move, and switch patterns if needed"""
        if self.ai_game.alien_pattern == AP.BOSSROOM:
            self._shoot_bullet()
            self._move_accordingly(boss_pattern)
            self._update_alien_bullets()
            if self.switch_time:
                self._switch_pattern()
            self.switch_cooldown += 1

    def _update_alien_bullets(self):
        """Update and delete if needed the bullets"""
        self.alien_bullets.update(speed = 7)
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height - 35:
                self.alien_bullets.remove(bullet)

    def _switch_pattern(self):
        """If the cooldown is up, switch patterns"""
        if self.switch_cooldown > 20 and self.delayed_frames >= self.delay_frames and self.rect.y <= 450:
            self.delay_frames = random.randint(5, 100)
            self.delayed_frames = 0
            self.switch_cooldown = 0
            self.switch_time = False
            if self.horde.ai_game.boss_pattern == BP.SHOOTBASIC: 
                self.needed_screen_hits = random.randint(2, 7)
                self.horde.ai_game.boss_pattern = BP.DARTTOHIT
            else:
                self.needed_screen_hits = random.randint(1, 5)
                self.horde.ai_game.boss_pattern = BP.SHOOTBASIC
        self.delayed_frames += 1

    def _move_accordingly(self, pattern):
        """Move based on the pattern"""
        if pattern == BP.SHOOTBASIC:
            self.x += 5.5 * self.xdirection
            self.rect.x = self.x
            if self.number_screen_hits >= self.needed_screen_hits:
                self.number_screen_hits = 0
                self.switch_time = True
            if self._check_screen_edges() == 0:
                self.xdirection *= -1
                self.rect.x -= 6 * self.xdirection
                self.number_screen_hits += 1
        elif pattern == BP.DARTTOHIT:
            if self._check_screen_edges() == 1:
                self.ydirection *= -1
                self.number_screen_hits += 1
                self.y += 60 * self.ydirection
                self.x += 150 * self.xdirection
                self.rect.y = self.y
                self.rect.x = self.x
                if self._check_screen_edges() == 0:
                    self.xdirection *= -1
                    self.x += 150 * self.xdirection
                    self.rect.x = self.x
            else:
                self.y += 5.5 * self.ydirection
                self.rect.y = self.y
                if self.rect.y <= 300 and self.number_screen_hits >= self.needed_screen_hits:
                    self.switch_time = True
                    self.number_screen_hits = 0
    
    def _check_screen_edges(self):
        """Check which, if any of the edges were hit"""
        if self.rect.left <= 0 or self.rect.right >= self.settings.screen_width:
            return(0)
        elif self.rect.bottom >= self.settings.screen_height or self.rect.top <= 0:
            return(1)

    def _shoot_bullet(self):
        """Shoot an alien_bullet"""
        if self.time_since_shot > 35:
            self.time_since_shot = 0
            new_bullet = AlienBullet(self.ai_game, self)
            self.alien_bullets.add(new_bullet)
        self.time_since_shot += 1
    
    def cut_scene(self):
        """Start the boss intro cutscene"""
        self.horde.ai_game.general_play = False
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("Games/Alien_Invasion/Music/Running_scared.wav")
        pygame.mixer.music.play(-1)
        self.start_time = time.time()
        self.rect.bottom = 0
        self.rect.centerx = self.ai_game.settings.screen_width / 2
        self.previous_step = 0
        self.check_cut_scene_movement()
        
    def check_cut_scene_movement(self):
        """Do the boss moves"""
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
            self.horde.ai_game.general_play = True
        