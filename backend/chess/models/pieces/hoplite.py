from chess.models.pieces.piece import Piece
from chess.models.types import Cell
import chess.constants.moves as Moves

class Hoplite(Piece):
    def __init__(self, position: Cell | None = None):
        super().__init__(position=position, piece_number=8, possibles_length=7*4*2)

    def get_moves(self) -> tuple:
        return Moves.HOPLITE

    def get_actions(self, board: 'AoWBoard', pos: Cell | None, turn: int, deny_enemy_king: bool = False) -> tuple:
        possibles, actions_mask = super().get_actions(board, pos, turn, deny_enemy_king)

        # add 2 to front move, when piece has not moved
        if self.has_moved():
            next_pos = Cell(pos[0] + 2, pos[1])
            possibles[4] = next_pos

        return possibles, actions_mask
