import pygame
from UI.all_enums import AlienPattern as AP
from UI.all_enums import BossPattern as BP
from Play_Screen.alien_bullet import AlienBullet
import time
import random
from pygame.sprite import Sprite
from Play_Screen.healthbar import HealthBar

class Boss(Sprite):
    def __init__(self, horde, health = 600, coords = (0, 0), directions = [1, 1]):
        """Initialize the Boss placement and things"""
        super().__init__()
        # To be fixed, odd names screwed up at some point
        self.ai_game = horde
        self.screen = horde.screen
        self.settings = horde.settings
        self.horde = horde
        # Image and rect things
        self.base_image = pygame.image.load("Games/Alien_Invasion/Images/alien_big.png")
        self.rect = self.base_image.get_rect()
        self.healthbar = HealthBar(self, "Galgazar, Destroyer of Moons")
        self.beam_rect = pygame.rect.Rect(0, 0, 2, 800)
        self.beam_color = (200, 255, 200)
        self.rect.center = coords
        self.x = self.rect.x
        self.y = self.rect.y
        # Health things
        self.max_hp = 600
        self.health = health
        # Shooting things
        self.alien_bullets = pygame.sprite.Group()
        self.time_since_shot = 0
        # Cutscene things
        self.previous_step = 0
        self.number_steps = 0
        # Speed and pattern things
        self.basic_speed = 5
            # 1 = right/down, left = -1/up
        self.xdirection = directions[0]
        self.ydirection = directions[1]
        self.all_patterns = {BP.SHOOTBASIC: random.randint(2, 4), 
                BP.DARTTOHIT: random.randint(1, 5), BP.BEAMATTACK: random.randint(4, 5)}
        self.shooter_patterns = (BP.SHOOTBASIC, BP.DARTTOHIT)
        # Switching pattern things
        self.switch_time = False
        self.number_screen_hits = 0
        self.needed_screen_hits = random.randint(1, 3)
        self.delay_frames = random.randint(5, 140)
        self.delayed_frames = 0
        # Beam things
        self.beam_active = False
        self.beam_cooldown = 0
        self.beam_hitbox = False
        # Start pattern and time
        self.time_start = time.time()
        self.boss_pattern = random.choice(list(self.all_patterns.keys()))
    
    def draw(self):
        """Draw the boss"""
        self.screen.blit(self.base_image, self.rect)
        if self.beam_active:
            self.screen.fill(self.beam_color, self.beam_rect)

    def update(self):
        """Shoot, move, and switch patterns if needed"""
        if self.boss_pattern in self.shooter_patterns:
            self._shoot_bullet()
        self._move_accordingly(self.boss_pattern)
        self._update_alien_bullets()
        if self.switch_time:
            self._switch_pattern()

    def _update_alien_bullets(self):
        """Update and delete if needed the bullets"""
        self.alien_bullets.update(speed = 7)
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height - 35:
                self.alien_bullets.remove(bullet)

    def _switch_pattern(self):
        """If the cooldown is up, switch patterns"""
        if self.delayed_frames >= self.delay_frames and self.rect.bottom <= 500:
            if self.boss_pattern == BP.BEAMATTACK:
                self._reset_beam()
            self.delay_frames = random.randint(5, 100)
            self.delayed_frames = 0
            self.switch_time = False
            self.available_patterns = self.all_patterns.copy()
            del self.available_patterns[self.boss_pattern]
            self.boss_pattern = random.choice(list(self.available_patterns.keys()))
            self.needed_screen_hits = self.available_patterns[self.boss_pattern]
            self.all_patterns = {BP.SHOOTBASIC: random.randint(2, 4), 
                BP.DARTTOHIT: random.randint(1, 5), BP.BEAMATTACK: random.randint(4, 5)}
            self.time_start = time.time()
        self.delayed_frames += 1

    def _move_accordingly(self, pattern):
        """Move based on the pattern"""
        if pattern == BP.SHOOTBASIC:
            self._shoot_basic_movement()
        elif pattern == BP.DARTTOHIT:
            self._dart_movement()
        elif pattern == BP.BEAMATTACK:
            self._beam_movement()

    def _shoot_basic_movement(self):
        """Basic side to side movement"""
        self.x += 5.5 * self.xdirection
        self.rect.x = self.x
        if self.number_screen_hits >= self.needed_screen_hits:
            self.number_screen_hits = 0
            self.switch_time = True
        if self._check_screen_edges() == 0:
            self.xdirection *= -1
            self.rect.x -= 6 * self.xdirection
            self.number_screen_hits += 1

    def _dart_movement(self):
        """The dart forward and back pattern movement"""
        # If it hits top/bottom, reverse, and move accordingly
        if self._check_screen_edges() == 1:
            self.ydirection *= -1
            self.number_screen_hits += 1
            self.y += 60 * self.ydirection
            self.x += 150 * self.xdirection
            self.rect.y = self.y
            self.rect.x = self.x
            if self._check_screen_edges() == 0:
                self.xdirection *= -1
                self.x += (self._amount_beyond_edge() + random.randint(5, 90)) * self.xdirection
                self.rect.x = self.x
        else:
            self.y += 5.5 * self.ydirection
            self.rect.y = self.y
            if self.rect.y <= 300 and self.number_screen_hits >= self.needed_screen_hits:
                self.switch_time = True
                self.number_screen_hits = 0

    def _beam_movement(self):
        """The pattern progression for firing the beam"""
        if not self.beam_active:
                self._fire_beam()
        elif self.beam_rect.width <= 30:
            self._beam_buildup()
        else:
            self.beam_hitbox = True
            self.x += 2.5 * self.xdirection
            self.rect.x = self.x
            self.beam_rect.top = self.rect.bottom
            self.beam_rect.centerx = self.rect.centerx + 1
            # Misleading name here, TB fixed later
            self.number_screen_hits = time.time() - self.time_start
            if self._check_screen_edges() == 0:
                self.xdirection *= -1
                self.rect.x -= 6 * self.xdirection
            elif self.number_screen_hits >= self.needed_screen_hits:
                self.switch_time = True
                self.number_screen_hits = 0

    def _reset_beam(self):
        """Put the rect and color back to the beginning"""
        self.beam_active = False
        self.beam_rect = pygame.rect.Rect(0, 0, 1, 800)
        self.beam_color = (200, 255, 200)
        self.beam_hitbox = False

    def _fire_beam(self):
        """Start the firing process"""
        self._beam_buildup()
        self.beam_active = True

    def _beam_buildup(self):
        """Widen the beam and darken the color"""
        if self.beam_cooldown >= 5:
            self.beam_rect = pygame.rect.Rect(self.beam_rect.x, 
                self.beam_rect.y, self.beam_rect.width + 1, 800)
            self.beam_color = (self.beam_color[0] - 5, 255, self.beam_color[2] - 5)
            self.beam_rect.top = self.rect.bottom
            self.beam_rect.centerx = self.rect.centerx + 1
            self.beam_cooldown = 0
        else: self.beam_cooldown += 1

    def _amount_beyond_edge(self):
        """Check how far beyond an edge the boss has gone"""
        if self.rect.left <= 0:
            return(self.rect.left * -1)
        elif self.rect.right >= self.settings.screen_width:
            return(self.rect.right - self.settings.screen_width)
        else:
            print("Something went wrong")
            return(150)
    
    def _check_screen_edges(self):
        """Check which, if any of the edges were hit"""
        if self.rect.left <= 0 or self.rect.right >= self.settings.screen_width:
            return(0)
        elif self.rect.bottom >= self.settings.screen_height or self.rect.top <= 0:
            return(1)

    def _shoot_bullet(self, cooldown = 35):
        """Shoot an alien_bullet"""
        if self.time_since_shot > cooldown:
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
            self.time_start = time.time()
        