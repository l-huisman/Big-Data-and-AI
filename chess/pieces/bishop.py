from constants import PieceType, Color

from .piece import Piece


class Bishop(Piece):
    def __init__(self, board, color: Color, x_position: int, y_position: int):
        super().__init__(board, color, PieceType.BISHOP, x_position, y_position)
        self._legal_moves = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    def get_possible_moves(self):
        self.moves = []
        self._check_legal_moves()
        return self.moves
