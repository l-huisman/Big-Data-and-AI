MOVE = -1
UPGRADE_PIECE = 1
DUTCH_WATERLINE = 2

CHECK_WIN = 10
CHECK_LOSE = -CHECK_WIN

CHECK_MATE_WIN = 100
CHECK_MATE_LOSE = -CHECK_MATE_WIN

DRAW = -50


# pieces
# These names should be a Capitalized representation of the piece name in the pieces array, e.g. "PAWN" for "pawn_1"
EMPTY = 0
PAWN = 1
BISHOP = 3
KNIGHT = 3
ROOK = 5
QUEEN = 9
WINGEDKNIGHT = KNIGHT + 2
HOPLITE = PAWN + 2
WARELEPHANT = BISHOP + 2
KING = 0
