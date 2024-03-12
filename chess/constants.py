# Constants
from enum import Enum

BOARD_SIZE = 8


class PieceType(Enum):
    KING = 0, 'K'
    QUEEN = 1, 'q'
    ROOK = 2, 'r'
    BISHOP = 3, 'b'
    KNIGHT = 4, 'k'
    PAWN = 5, 'p'

    def __init__(self, value, letter):
        self._value_ = value
        self.letter = letter


class Color(Enum):
    WHITE = -1
    BLACK = 1
