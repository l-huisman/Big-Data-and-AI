from aow.models.pieces.piece import Piece
from aow.models.types import Cell
import aow.constants.moves as Moves

class Bishop(Piece):
    def __init__(self, position: Cell | None = None):
        super().__init__(position=position, piece_number=2, possibles_length=7*4)

    def get_moves(self) -> tuple:
        return Moves.BISHOP
