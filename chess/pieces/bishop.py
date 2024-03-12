from constants import PieceType, Color

from .piece import Piece


class Bishop(Piece):
    def __init__(self, board, color: Color, x_position: int, y_position: int):
        super().__init__(board, color, PieceType.BISHOP, x_position, y_position)

    def get_possible_moves(self):
        self.moves = []
        self.__check_diagonals()
        return self.moves

    def __check_diagonals(self):
        self._calculate_diagonals(1, 1)
        self._calculate_diagonals(-1, 1)
        self._calculate_diagonals(1, -1)
        self._calculate_diagonals(-1, -1)
