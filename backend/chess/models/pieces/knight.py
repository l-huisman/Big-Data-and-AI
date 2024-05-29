from chess.models.pieces.piece import Piece
from chess.models.types import Cell


class Knight(Piece):
    def __init__(self, position: Cell | None = None):
        super().__init__(position=position, piece_number=3, possibles_length=2*4, can_jump=True)
