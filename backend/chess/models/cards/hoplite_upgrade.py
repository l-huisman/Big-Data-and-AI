from chess.models import Cell
from chess.models.cards.upgrade_card import UpgradeCard
from chess.models.pieces import Rook, Knight, Pawn


class HopliteUpgradeCard(UpgradeCard):
    def __init__(self):
        super().__init__(costs=2, piece_to_upgrade=Pawn())

    def get_actions(self, board: 'AoWBoard', pos: Cell | None, turn: int, deny_enemy_king: bool = False) -> tuple:
        source_pos, possibles, actions_mask, pieces = self.get_empty_upgrade_actions(turn, board)
        if board.get_resources(turn) >= self.get_cost():
            for i, piece in enumerate(pieces):
                if board.pieces[turn][piece] is None:
                    continue

                possibles[i] = board.pieces[turn][piece]
                actions_mask[i] = 1

        return source_pos, possibles, actions_mask
