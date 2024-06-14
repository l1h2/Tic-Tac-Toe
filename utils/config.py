import enum


class States(enum.Enum):
    X_TURN = "X's Turn"
    O_TURN = "O's Turn"
    X_WIN = "X Wins!"
    O_WIN = "O Wins!"
    DRAW = "It's a Draw!"


class Players(enum.Enum):
    X = 1
    O = -1


class PlayerType(enum.Enum):
    HUMAN = 0
    COMPUTER = 1


class Wins(enum.Enum):
    COL = 0
    ROW = 1
    DIAG = 2
    DIAG_2 = 3


GameBoard = list[list[Players | None]]
