import enum

class ChangeSpeedStates(enum.Enum):
    ONEGROUP = enum.auto()
    FIRSTTWO = enum.auto()
    LASTTWO = enum.auto()
    ENDTWO = enum.auto()
    ALLTHREE = enum.auto()
    FIRSTCOLUMN = enum.auto()
    SECONDCOLUMN = enum.auto()
    THIRDCOLUMN = enum.auto()