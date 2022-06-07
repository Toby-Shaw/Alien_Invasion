from UI.text import Text

class InfoBoard:
    """For creating all the images and text pieces on the Information page"""
    def __init__(self, ai_game):
        """Initialize the text pieces"""
        
        self.strong_bullet_info = Text(ai_game, 
        """Strong Bullet is an activatable ability that
        allows your bullets to  pierce multiple enemies.
        Activate it with the down key or S""", 
            40, (0, 0, 0), 550, 100)
        self.shield_info = Text(ai_game, 
        """Warp Shield is an activatable ability that
        blocks up to two bullets  from the enemies before breaking.
        Activate it with the up key or W.""",
            40, (0, 0, 0), 550, 250)