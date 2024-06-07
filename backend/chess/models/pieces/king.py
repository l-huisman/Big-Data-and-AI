import chess.constants.moves as Moves
from chess.game.check import Check
from chess.models.pieces.piece import Piece
from chess.models.pieces.rook import Rook
from chess.models.types import Cell
from chess.utils.cell import CellUtils


class King(Piece):
    def __init__(self, position: Cell | None = None):
        super().__init__(position=position, piece_number=6, possibles_length=10)

    def get_moves(self) -> tuple:
        return Moves.KING

    def get_actions(self, board: 'AoWBoard', pos: Cell | None, turn: int, deny_enemy_king: bool = False) -> tuple:
        pos = CellUtils.make_cell(pos)
        possibles, actions_mask = self.get_empty_actions()

        for i, (r, c) in enumerate(Moves.KING):
            next_pos = Cell(pos.row + r, pos.col + c)

            if not board.is_valid_move(Cell(pos.row, pos.col), next_pos, turn, False):
                continue

            if self.is_neighbor_enemy_king(next_pos, turn, board):
                continue

            can_castle_right = self.can_castle(turn, pos, Cell(pos.row, pos.col + 3), board)
            can_castle_left = self.can_castle(turn, pos, Cell(pos.row, pos.col - 4), board)

            # temp since it removes king?
            if i == 8 or i == 9:
                continue

            if i == 8 and not can_castle_right:
                continue

            if i == 9 and not can_castle_left:
                continue

            possibles[i] = next_pos
            actions_mask[i] = 1
        return possibles, actions_mask

    def can_castle(self, turn: int, king_pos: Cell, rook_pos: Cell, board: 'AoWBoard') -> bool:
        king_pos = CellUtils.make_cell(king_pos)
        rook_pos = CellUtils.make_cell(rook_pos)

        if not board.is_in_range(king_pos) or not board.is_in_range(rook_pos):
            return False

        if not board.is_piece(turn, rook_pos, Rook()) or not board.is_piece(turn, Cell(0, 4), King()):
            return False

        if Check(board).is_check(king_pos, turn):
            return False

        if self.has_moved() or (king_pos.row != 0 and king_pos.col != 4):
            return False

        if not board.is_path_empty(king_pos, rook_pos, turn):
            return False

        # check if rook has moved
        if not board.get_piece(rook_pos, turn).has_moved():
            return False

        return True

    @staticmethod
    def is_neighbor_enemy_king(pos: Cell, turn: int, board: 'AoWBoard') -> bool:
        row, col = pos
        row_enemy_king, col_enemy_king = board.get_king_position(1 - turn)
        row_enemy_king = 7 - row_enemy_king
        diff_row = abs(row - row_enemy_king)
        diff_col = abs(col - col_enemy_king)
        return diff_row <= 1 and diff_col <= 1

