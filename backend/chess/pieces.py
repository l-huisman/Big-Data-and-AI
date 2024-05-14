from chess.types import Cell

EMPTY = 0
PAWN = 1
BISHOP = 2
KNIGHT = 3
ROOK = 4
QUEEN = 5
KING = 6

# new pieces
WINGED_KNIGHT = 7
HOPLITE = 8
WARELEFANT = 9

BLACK = 0
WHITE = 1

ASCIIS = (
    ("♙", "♗", "♘", "♖", "♕", "♔", "☺", "♨", "♩"),
    ("♟︎", "♝", "♞", "♜", "♛", "♚", "☻", "♆", "♫"),
)


def get_ascii(color: int, piece: int) -> str:
    return ASCIIS[color][piece - 1][0]


def get_piece_name(piece: int) -> str:
    return {
        EMPTY: "empty",
        PAWN: "pawn",
        BISHOP: "bishop",
        KNIGHT: "knight",
        ROOK: "rook",
        QUEEN: "queen",
        KING: "king",
        WINGED_KNIGHT: "winged_knight",
        HOPLITE: "hoplite",
        WARELEFANT: "warelefant",
    }[piece]
