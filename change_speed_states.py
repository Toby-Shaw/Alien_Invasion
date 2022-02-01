import enum

class ChangeSpeedStates(enum.Enum):
    ONEGROUP = (0, 1 ,2)
    FIRSTTWO = (0, 1)
    LASTTWO = (1, 2)
    ENDTWO = (0, 2)
    FIRSTCOLUMN = (0,)
    SECONDCOLUMN = (1,)
    THIRDCOLUMN = (2,)