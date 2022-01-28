class Gamestats:
    """Track stats for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score never resets.
        f = open("Games/Alien_Invasion/high_score.txt", "r")
        self.high_score = int(f.read())

    def reset_stats(self):
        """Initialize stats that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.current_fps = 100
        self.tick_update = 0