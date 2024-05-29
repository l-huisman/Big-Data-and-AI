import chess.models.pieces.piece as Piece
from chess.models.types import Cell


class Empty(Piece):
    def __init__(self, position: Cell):
        super().__init__(position, piece_number=0, possibles_length=0)
