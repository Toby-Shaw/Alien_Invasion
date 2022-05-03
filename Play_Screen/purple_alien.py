from Play_Screen.alien import Alien
from UI.all_enums import AlienColors as AC

class Purple_Alien(Alien):

    def __init__(self, ai_game):
        """Initialize the purple alien, gets the base alien things"""
        super().__init__(ai_game, color=AC.PURPLE)