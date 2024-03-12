from .piece import Piece
from constants import PieceType, Color


class Knight(Piece):
    def __init__(self, board, color: Color, x_position: int, y_position: int):
        super().__init__(board, color, PieceType.KNIGHT, x_position, y_position)
        self._legal_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

    def get_possible_moves(self):
        self.moves = []
        self._check_legal_moves()
        return self.moves

