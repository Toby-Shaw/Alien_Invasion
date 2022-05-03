from enum import Enum

class CollisionsStates(Enum):
    ONEGROUP = (0, 1, 2)
    FIRSTTWO = (0, 1)
    TWOTHREE = (1, 2)
    ONETHREE = (0, 2)
    ONEFOUR = (0, 3)
    TWOFOUR = (1, 3)
    THREEFOUR = (2, 3)
    # Second value of the tuples is for distinction in lists for left/right
    FIRSTCOLUMNLEFT = (0, 10)
    FIRSTCOLUMNRIGHT = (0, 20)
    SECONDCOLUMNLEFT = (1, 10)
    SECONDCOLUMNRIGHT = (1, 20)
    THIRDCOLUMNLEFT = (2, 10)
    THIRDCOLUMNRIGHT = (2, 20)
    FOURTHCOLUMNLEFT = (3, 10)
    FOURTHCOLUMNRIGHT = (3, 20)

class AlienPattern(Enum):
    BASIC = (0, 0)
    # 2nd number only really matters for TWO THREE, and FOUR, 
    # helps shorten code as a list index for a column shell list
    # Third number helps shorten assigning aliens to columns
    TWOROWS = (0.5, 1, 2)
    THREEROWS = (1, 0, 3)
    FOURROWS = (0.7, 2, 4)
    BOSSROOM = (2, 0)
    PURPLE = (3, 0)

class GameStates(Enum):
    MAINMENU = 1
    PLAYSCREEN = 2
    PAUSEMENU = 3
    INFOSCREEN = 4
    ENDSCREEN = 5
    SETTINGS = 6
    HIGHSCORES = 7
    INPUTPAGE = 8

class BossPattern(Enum):
    SHOOTBASIC = 1
    DARTTOHIT = 2
    BEAMATTACK = 3
    MACHINEGUN = 5
    DARTWITHFASTFIRE = 10
    DIAGONAL = 6

class AlienColors(Enum):
    GREEN = 1
    RED = 2
    PURPLE = 3