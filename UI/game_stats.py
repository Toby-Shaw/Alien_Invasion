class Gamestats:
    """Track stats for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score never resets.
        self.get_high_score()

    def get_high_score(self):
        """Read the high score from the file in a correct manner"""
        f = open("Games/Alien_Invasion/high_score.txt", "r")
        high_score = str(f.read())
        self.high_score = high_score.split()
        stop_index = self.high_score.index('/')
        self.high_initials = self.high_score[stop_index + 1:]
        self.high_score = self.high_score[0:stop_index]
        #print(self.high_score)
        #print(self.high_initials)
        for x in range(len(self.high_score)):
            self.high_score[x] = int(self.high_score[x])

    def reset_stats(self):
        """Initialize stats that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.current_fps = 100
        self.tick_update = 0