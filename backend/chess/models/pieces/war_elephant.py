import chess.constants.moves as Moves
from chess.models.pieces.piece import Piece
from chess.models.types import Cell


class Warelephant(Piece):
    def __init__(self, position: Cell | None = None):
        super().__init__(position=position, piece_number=9, possibles_length=7 * 4, can_jump=True)

    def get_moves(self) -> tuple:
        return Moves.WARELEPHANT
