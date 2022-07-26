from UI.text import Text

class InfoBoard:
    """For creating all the images and text pieces on the Information page"""
    def __init__(self, ai_game):
        """Initialize the text pieces"""
        black = (0, 0, 0)
        center = 600
        self.strong_bullet_info = Text(ai_game, 
        """Strong Bullet is an activatable ability that
        allows your bullets to  pierce multiple enemies.
        Activate it with the down key or S.""", 
            40, black, center, 400)
        self.shield_info = Text(ai_game, 
        """Warp Shield is an activatable ability that
        blocks up to two bullets  from the enemies before breaking.
        Activate it with the up key or W.""",
            40, black, center, 500)
        self.control_info = Text(ai_game, 
        """Use Keys A and D (or left and right arrows)  to control the movement
        of your ship across the screen.""", 40, black, center, 300)
        self.summary = Text(ai_game, 
        """You are fighting against evil aliens that  
        seek to destroy Earth!""", 40, black, center, 100)
        self.bullet_info = Text(ai_game,
        """Use your space bar to fire bullets  
        at the monsters that attack you.""", 40, black, center, 200)
        self.all_text = [self.strong_bullet_info, self.shield_info, self.control_info, 
                self.summary, self.bullet_info]