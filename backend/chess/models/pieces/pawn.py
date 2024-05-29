import chess.models.pieces.piece as Piece
from chess.models.types import Cell


class Pawn(Piece):
    def __init__(self, position: Cell):
        super().__init__(position, piece_number=1, possibles_length=7 * 4 * 2)
