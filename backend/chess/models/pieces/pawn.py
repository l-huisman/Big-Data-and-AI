from chess.models.pieces.piece import Piece
from chess.models.types import Cell


class Pawn(Piece):
    def __init__(self, position: Cell | None = None):
        super().__init__(position=position, piece_number=1, possibles_length=7 * 4 * 2)
