from pygame.mixer import Sound, Channel
from pygame.mixer import music

class GameSounds:

    def __init__(self, mute = False):
        """Initialize the music and initial volumes, play the music"""
        music.load("Games/Alien_Invasion/Music/cinematic-space-drone-10623.wav")
        music.set_volume(0.9)
        music.play(-1)
        self.shield_hit = Sound("Games/Alien_Invasion/Music/shield_hit.wav")
        self.shield_hit.set_volume(0.5)
        self.shield_up = Sound("Games/Alien_Invasion/Music/shield_up.wav")
        self.shield_up.set_volume(0.5)
        self.start_sound = Sound("Games/Alien_Invasion/Music/Start_sound.wav")
        self.start_sound.set_volume(0.7)
        self.strong_start = Sound("Games/Alien_Invasion/Music/strong_bullet_up.wav")
        self.start_sound.set_volume(0.4)
        self.bullet_fired = Sound("Games/Alien_Invasion/Music/laserShoot.wav")
        self.bullet_fired.set_volume(0.15)
        self.ship_hit = Sound("Games/Alien_Invasion/Music/ship_hit.wav")
        self.ship_hit.set_volume(0.75)
        self.sound_channel = Channel(0)
        if mute:
            self.sound_channel.set_volume(0)
            music.set_volume(0)

    def change_back(self):
        """change back to the default music"""
        music.stop()
        music.unload()
        music.load("Games/Alien_Invasion/Music/cinematic-space-drone-10623.wav")
        music.play(-1)