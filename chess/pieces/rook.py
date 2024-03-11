from .piece import Piece
from constants import PieceType, Color


class Rook(Piece):
    def __init__(self, board, color: Color, x_position: int, y_position: int):
        super().__init__(board, color, PieceType.ROOK, x_position, y_position)

    def get_possible_moves(self):
        self.moves = []
        self.__check_horizontals()
        return self.moves

    def __check_horizontals(self):
        self._calulate_horizontals(1, 0)
        self._calulate_horizontals(-1, 0)
        self._calulate_horizontals(0, 1)
        self._calulate_horizontals(0, -1)
