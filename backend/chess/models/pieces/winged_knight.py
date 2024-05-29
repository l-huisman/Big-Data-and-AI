import chess.models.pieces.piece as Piece
from chess.models.types import Cell


class WingedKnight(Piece):
    def __init__(self, position: Cell):
        super().__init__(position, piece_number=7, possibles_length=3*4)
