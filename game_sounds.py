from pygame.mixer import Sound, Channel
from pygame.mixer import music

class GameSounds:

    def __init__(self):
        """Initialize the music and initial volumes, play the music"""
        music.load("Games\Alien_Invasion\Music\cinematic-space-drone-10623.wav")
        music.set_volume(0.5)
        music.play()
        self.shield_hit = Sound("Games/Alien_Invasion/Music/shield_hit.wav")
        self.shield_hit.set_volume(0.5)
        self.shield_up = Sound("Games/Alien_Invasion/Music/shield_up.wav")
        self.shield_up.set_volume(0.5)
        self.start_sound = Sound("Games/Alien_Invasion/Music/Start_sound.wav")
        self.start_sound.set_volume(0.7)
        self.strong_start = Sound("Games/Alien_Invasion/Music/strong_bullet_up.wav")
        self.start_sound.set_volume(0.4)
        self.bullet_fired = Sound("Games/Alien_Invasion/Music/bullet_fired.wav")
        self.bullet_fired.set_volume(0.5)
        self.ship_hit = Sound("Games/Alien_Invasion/Music/ship_hit.wav")
        self.sound_channel = Channel(0)