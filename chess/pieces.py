from chess.types import Cell

EMPTY = 0
PAWN = 1
BISHOP = 2
KNIGHT = 3
ROOK = 4
QUEEN = 5
KING = 6

WINGED_KNIGHT = 7
HOPLITE = 8

BLACK = 0
WHITE = 1

ASCIIS = (
    ("♙", "♗", "♘", "♖", "♕", "♔", "☺", "𓐬"),
    ("♟︎", "♝", "♞", "♜", "♛", "♚", "☻", "𓐭"),
)


def get_ascii(color: int, piece: int):
    return ASCIIS[color][piece - 1][0]
