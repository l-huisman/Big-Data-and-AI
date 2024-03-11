from board import Board
from piece import Piece
from constants import PieceType, Color


class Queen(Piece):
    def __init__(self, board: Board, color: Color, x_position: int, y_position: int):
        super().__init__(board, color, PieceType.QUEEN, x_position, y_position)

    def get_possible_moves(self):
        self.moves = []
        self.__check_moves()
        return self.moves

    def __check_moves(self):
        self._calulate_horizontals(1, 0)
        self._calulate_horizontals(-1, 0)
        self._calulate_horizontals(0, 1)
        self._calulate_horizontals(0, -1)
        self._calculate_diagonals(1, 1)
        self._calculate_diagonals(-1, 1)
        self._calculate_diagonals(1, -1)
        self._calculate_diagonals(-1, -1)
