from pieces import Piece
from constants import PieceType, Color


class Pawn(Piece):
    __in_starting_position = True

    def __init__(self, board, color: Color, x_position: int, y_position: int):
        super().__init__(board, color, PieceType.PAWN, x_position, y_position)
        self.__legal_moves = [(-1, (1 * self.color.value)), (1, 1 * self.color.value)]

    def get_possible_moves(self) -> list:
        self.moves = []
        self.__check_moves()
        self.__check_diagonals()
        return self.moves

    def __check_moves(self) -> None:
        if (
            self.board.get_piece_at_position(
                self.x_position, self.y_position + (1 * self.color.value)
            )
            == False
        ):
            self.moves.append(
                (self.x_position, self.y_position + (1 * self.color.value))
            )
        if self.__in_starting_position:
            if (
                self.board.get_piece_at_position(
                    self.x_position, self.y_position + (2 * self.color.value)
                )
                == False
            ):
                self.moves.append(
                    (self.x_position, self.y_position + (2 * self.color.value))
                )

    def __check_diagonals(self) -> None:
        for move in self.__legal_moves:
            x = self.x_position + move[0]
            y = self.y_position + move[1]
            if x < 0 or x > 7 or y < 0 or y > 7:
                continue
            piece_at_position = self.board.get_piece_at_position(x, y)
            if piece_at_position == None:
                continue
            elif piece_at_position.color != self.color:
                self.moves.append((x, y))
            else:
                continue
