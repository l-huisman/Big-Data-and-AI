from .piece import Piece
from constants import PieceType, Color


class Queen(Piece):
    def __init__(self, board, color: Color, x_position: int, y_position: int):
        super().__init__(board, color, PieceType.QUEEN, x_position, y_position)
        self._legal_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

    def get_possible_moves(self):
        self.moves = []
        self._check_legal_moves()
        return self.moves
    
    def _check_legal_moves(self) -> None:
        for move in self._legal_moves:
            self._check_straights(move[0], move[1])
