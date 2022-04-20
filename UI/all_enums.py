from enum import Enum

class CollisionsStates(Enum):
    ONEGROUP = (0, 1, 2)
    FIRSTTWO = (0, 1)
    LASTTWO = (1, 2)
    ENDTWO = (0, 2)
    # Second value of the tuples is for distinction in lists for left/right
    FIRSTCOLUMNLEFT = (0, 3)
    FIRSTCOLUMNRIGHT = (0, 4)
    SECONDCOLUMNLEFT = (1, 3)
    SECONDCOLUMNRIGHT = (1, 4)
    THIRDCOLUMNLEFT = (2, 3)
    THIRDCOLUMNRIGHT = (2, 4)
    FOURTHCOLUMNLEFT = (3, 3)
    FOURTHCOLUMNRIGHT = (3, 4)

class AlienPattern(Enum):
    BASIC = (0, 0)
    # 2nd number only really matters for TWO THREE, and FOUR, helps shorten code as a list index for a column shell list
    TWOROWS = (0.5, 1)
    THREEROWS = (1, 0)
    FOURROWS = (0.7, 2)
    BOSSROOM = (2, 0)

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