from aow.models.pieces.war_elephant import Warelephant
from aow.models.pieces.piece import Piece
from aow.models.types import Cell
import aow.constants.moves as Moves

class Rook(Piece):
    def __init__(self, position: Cell | None = None):
        super().__init__(position=position, piece_number=4, possibles_length=7 * 4, upgradable=True,
                         upgrade_options=[Warelephant()])

    def get_moves(self) -> tuple:
        return Moves.ROOK
