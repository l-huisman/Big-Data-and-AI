import numpy as np

from chess.models.cards.card import Card
from chess.models.pieces import Piece


class UpgradeCard(Card):
    def __init__(self, costs: int, piece_to_upgrade: Piece):
        super().__init__(costs)
        self.piece_to_upgrade = piece_to_upgrade

    def get_empty_upgrade_actions(self, turn: int, board: 'AoWBoard'):
        pieces = [key for key in board.pieces[turn].keys() if
                  key.split("_")[0] == self.piece_to_upgrade.get_name().lower()]

        possibles = np.zeros((len(pieces), 2), dtype=np.int32)
        actions_mask = np.zeros(len(pieces), dtype=np.int32)
        source_pos = np.zeros((len(pieces), 2), dtype=np.int32)

        for i, piece in enumerate(pieces):
            if board.pieces[turn][piece] is None:
                continue

            possibles[i] = [0, 0]
            source_pos[i] = board.pieces[turn][piece]

        return source_pos, possibles, actions_mask, pieces
