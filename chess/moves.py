POSSIBLE_MOVES = {
    "king": 8,
    "knight": 8,
    "rook": 7 * 4,
    "bishop": 7 * 4,
    "queen": 7 * 4 * 2,
    "pawn": 7 * 4 * 2,
}

KING = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

ROOK = (
    (1, 0),
    (2, 0),
    (3, 0),
    (4, 0),
    (5, 0),
    (6, 0),
    (7, 0),
    (-1, 0),
    (-2, 0),
    (-3, 0),
    (-4, 0),
    (-5, 0),
    (-6, 0),
    (-7, 0),
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (0, 5),
    (0, 6),
    (0, 7),
    (0, -1),
    (0, -2),
    (0, -3),
    (0, -4),
    (0, -5),
    (0, -6),
    (0, -7),
)
BISHOP = (
    (1, 1),
    (1, -1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (2, -2),
    (3, -3),
    (4, -4),
    (5, -5),
    (6, -6),
    (7, -7),
    (-1, 1),
    (-2, 2),
    (-3, 3),
    (-4, 4),
    (-5, 5),
    (-6, 6),
    (-7, 7),
    (-1, -1),
    (-2, -2),
    (-3, -3),
    (-4, -4),
    (-5, -5),
    (-6, -6),
    (-7, -7),
)

KNIGHT = (
    (2, 1),
    (2, -1),
    (-2, 1),
    (-2, -1),
    (1, 2),
    (1, -2),
    (-1, 2),
    (-1, -2),
)

WINGED_KNIGHT = (
    (2, 1),
    (2, -1),
    (-2, 1),
    (-2, -1),
    (1, 2),
    (1, -2),
    (-1, 2),
    (-1, -2),
    (2, 2),
    (2, -2),
    (-2, 2),
    (-2, -2),
)

QUEEN = BISHOP + ROOK

PAWN = ((1, 0), (2, 0), (1, 1), (1, -1)) # + ROOK [2:] + BISHOP [1:]?????
HOPLITE = ((1, 0), (2, 0), (1, 1), (1, -1), (0, 1))

PIECE_MOVE = [
    None,
    PAWN,
    BISHOP,
    KNIGHT,
    ROOK,
    QUEEN,
    KING,
    WINGED_KNIGHT,
    HOPLITE,
]
