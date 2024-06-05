import chess.constants.moves as Moves
from chess.models.pieces.piece import Piece
from chess.models.types import Cell


class King(Piece):
    def __init__(self, position: Cell | None = None):
        super().__init__(position=position, piece_number=6, possibles_length=8)

    def get_moves(self) -> tuple:
        return Moves.KING

    def get_actions(self, board: 'AoWBoard', pos: Cell | None, turn: int, deny_enemy_king: bool = False) -> tuple:
        var1, var2 = super().get_actions(board, pos, turn, deny_enemy_king=True)
        # print(var1, var2)
        return var1, var2
