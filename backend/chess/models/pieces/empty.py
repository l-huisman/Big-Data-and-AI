from chess.models.pieces.piece import Piece
from chess.models.types import Cell


class Empty(Piece):
    def __init__(self, position: Cell | None = None):
        super().__init__(position=position, piece_number=0, possibles_length=0)
