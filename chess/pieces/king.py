from .piece import Piece
from constants import PieceType, Color


class King(Piece):
    def __init__(self, board, color: Color, x_position: int, y_position: int):
        super().__init__(board, color, PieceType.KING, x_position, y_position)
        self._legal_moves = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

    def get_possible_moves(self):
        self.moves = []
        self._check_legal_moves()
        # TODO: Add castling
        return self.moves
