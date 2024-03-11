# Constants
from enum import Enum

BOARD_SIZE = 8

class PieceType(Enum):
    KING = 0
    QUEEN = 1
    ROOK = 2
    BISHOP = 3
    KNIGHT = 4
    PAWN = 5


class Color(Enum):
    WHITE = -1
    BLACK = 1
