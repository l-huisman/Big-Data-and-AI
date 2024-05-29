import chess.models.pieces.piece as Piece
from chess.models.types import Cell


class WarElephant(Piece):
    def __init__(self, position: Cell):
        super().__init__(position, piece_number=9, possibles_length=7*4)
