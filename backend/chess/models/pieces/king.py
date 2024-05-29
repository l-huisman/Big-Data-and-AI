from chess.models.pieces.piece import Piece
from chess.models.types import Cell


class King(Piece):
    def __init__(self, position: Cell | None = None):
        super().__init__(position=position, piece_number=6, possibles_length=8)
