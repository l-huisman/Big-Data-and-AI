import chess.constants.moves as Moves
from chess.models.pieces.piece import Piece
from chess.models.types import Cell


class King(Piece):
    def __init__(self, position: Cell | None = None):
        super().__init__(position=position, piece_number=6, possibles_length=8)

    def get_moves(self) -> tuple:
        return Moves.KING
