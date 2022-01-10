class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        # Alien settings
        self.fleet_drop_speed = 10

        #How quickly the game speeds up
        self.speedup_scale = 1.25

        # How quickly alien point values increase
        self.score_scale = 1.5

        # How many strong bullets are allowed per powerup
        self.strong_bullets_allowed = 6

        # Shooter alien stuff
        self.alien_bullet_color = (0, 255, 0)
        self.alien_bullet_width = 6
        self.alien_bullet_height = 15
        self.alien_bullet_speed = 2.0
        self.alien_bullets_allowed = 4

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the settings that change during the game"""
        self.bullet_width = 4
        self.normal_bullet = True
        self.bullet_color = (60, 60, 60)
        self.ship_speed = 2.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        self.bullet_height = 15
        self.bullets_allowed = 4

        # Strong bullet timer
        self.strong_bullets_fired = 0
        self.cooldown_start = False
        self.cooldown_up = True
        self.cooldown = 0

        # fleet_direction of 1 represents right, -1 = left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        if self.ship_speed < 8:
            self.bullet_height *= (self.speedup_scale - 0.2)
            self.ship_speed *= self.speedup_scale
            self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)

    def strong_bullet(self):
        """Begin the strong bullet powerup"""
        self.strong_bullets_fired = 0
        self.bullet_speed *= 2
        self.bullets_allowed = 2
        self.bullet_color = (255, 0, 0)
        self.bullet_width = 8
        self.normal_bullet = False

    def normal_bullet_reset(self):
        """Reset to normal bullet settings once the cooldown is up"""
        if not self.normal_bullet:
            self.bullets_allowed = 4
            self.bullet_speed /= 2
            self.bullet_color = (60, 60, 60)
            self.bullet_width = 4
            self.normal_bullet = True

