import enum

class CollisionsStates(enum.Enum):
    ONEGROUP = (0, 1 ,2)
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