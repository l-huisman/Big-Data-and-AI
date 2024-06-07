from chess.models.pieces.piece import Piece
from chess.models.pieces.queen import Queen
from chess.models.types import Cell
import chess.constants.moves as Moves

class Hoplite(Piece):
    def __init__(self, position: Cell | None = None):
        super().__init__(position=position, piece_number=8, possibles_length=7*4*2, upgradable=True, upgrade_options=[Queen()])

    def get_moves(self) -> tuple:
        return Moves.HOPLITE

    def get_actions(self, board: 'AoWBoard', pos: Cell | None, turn: int, deny_enemy_king: bool = False) -> tuple:
        possibles, actions_mask = self.get_empty_actions()

        if pos is None and self.position is None:
            return possibles, actions_mask

        if pos is None:
            pos = self.position

        # add 1 to front move
        if board.is_valid_move(pos, Cell(pos[0] + 1, pos[1]), turn, deny_enemy_king):
            next_pos = Cell(pos[0] + 1, pos[1])
            possibles[0] = next_pos
            actions_mask[0] = 1

        # 1 to right move
        if (board.is_valid_move(pos, Cell(pos[0] + 1, pos[1] + 1), turn, deny_enemy_king) and
                board.is_enemy_piece(Cell(pos[0] + 1, pos[1] + 1), turn)):
            next_pos = Cell(pos[0] + 1, pos[1] + 1)
            possibles[1] = next_pos
            actions_mask[1] = 1

        # 1 to left move
        if (board.is_valid_move(pos, Cell(pos[0] + 1, pos[1] - 1), turn, deny_enemy_king) and
                board.is_enemy_piece(Cell(pos[0] + 1, pos[1] - 1), turn)):
            next_pos = Cell(pos[0] + 1, pos[1] - 1)
            possibles[2] = next_pos
            actions_mask[2] = 1

        # add 2 to front move, when piece has not moved
        if (not self.has_moved() and board.is_valid_move(pos, Cell(pos[0] + 2, pos[1]), turn, deny_enemy_king) and
                board.is_tile_empty_on_both_side(Cell(pos[0] + 1, pos[1]), turn) and
                board.is_tile_empty_on_both_side(Cell(pos[0] + 2, pos[1]), turn)):
            next_pos = Cell(pos[0] + 2, pos[1])
            possibles[3] = next_pos
            actions_mask[3] = 1

        return possibles, actions_mask
