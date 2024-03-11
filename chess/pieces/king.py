from .piece import Piece
from constants import PieceType, Color


class King(Piece):
    def __init__(self, board, color: Color, x_position: int, y_position: int):
        super().__init__(board, color, PieceType.KING, x_position, y_position)
        self.__legal_moves = [
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
        ]

    def get_possible_moves(self):
        self.moves = []
        self.__check_moves()
        # TODO: Add castling
        return self.moves

    def __check_moves(self):
        for move in self.__legal_moves:
            x = self.x_position + move[0]
            y = self.y_position + move[1]
            if x < 0 or x > 7 or y < 0 or y > 7:
                continue
            piece_at_position = self.board.get_piece_at_position(x, y)
            if piece_at_position == None:
                self.moves.append((x, y))
            elif piece_at_position.color != self.color:
                self.moves.append((x, y))
