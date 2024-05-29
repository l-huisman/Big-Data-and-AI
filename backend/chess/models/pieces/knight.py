import chess.models.pieces.piece as Piece
from chess.models.types import Cell


class Knight(Piece):
    def __init__(self, position: Cell):
        super().__init__(position, piece_number=3, possibles_length=2*4)
