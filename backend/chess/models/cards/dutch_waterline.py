import numpy as np

from chess.models import Cell
from chess.models.cards.action_card import ActionCard
from chess.models.pieces import King, Empty
from chess.utils.cell import CellUtils


class DutchWaterline(ActionCard):
    def __init__(self):
        super().__init__(1)

    def get_actions(self, pos: Cell, board: 'AoWBoard', turn: int) -> tuple:
        possibles = np.zeros((4, 2), dtype=np.int32)
        source_pos = np.zeros((4, 2), dtype=np.int32)

        if board.get_resources(turn) < self.get_cost() or self.is_played():
            return possibles, source_pos, np.zeros(4, dtype=np.int32)

        for index, row in enumerate(range(2, 6)):
            possibles[index] = [0, 7]
            source_pos[index] = [row, 0]

        action_mask = np.ones(4, dtype=np.int32)
        return possibles, source_pos, action_mask

    def play(self, pos: Cell, board: 'AoWBoard', turn: int):
        assert board.get_resources(turn) >= self.get_cost() and not self.is_played(), \
            "The card cannot be played, because the resources are not enough or it was already played"

        self.set_played()
        board.remove_resources(turn, self.get_cost())
        pos = CellUtils.make_cell(pos)
        row = pos.row
        row_turn1 = 7 - row
        for turn in range(2):
            for col in range(8):
                # Check if the piece is a king before removing it
                row = row if turn == 0 else row_turn1
                if not board.is_piece(turn, Cell(row, col), King()):
                    board.set_piece(turn, Cell(row, col), Empty())
