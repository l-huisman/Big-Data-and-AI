import aow.constants.moves as Moves
from aow.models.pieces.piece import Piece
from aow.models.pieces.winged_knight import Wingedknight
from aow.models.types import Cell


class Knight(Piece):
    def __init__(self, position: Cell | None = None):
        super().__init__(position=position, piece_number=3, possibles_length=2 * 4, can_jump=True, upgradable=True,
                         upgrade_options=[Wingedknight()])

    def get_moves(self) -> tuple:
        return Moves.KNIGHT
