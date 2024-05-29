from chess.models.pieces.piece import Piece
from chess.models.types import Cell


class WingedKnight(Piece):
    def __init__(self, position: Cell | None = None):
        super().__init__(position=position, piece_number=7, possibles_length=3*4, can_jump=True)
