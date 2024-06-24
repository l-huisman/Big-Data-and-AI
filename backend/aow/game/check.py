from aow.models import Cell
from aow.models.pieces.bishop import Bishop
from aow.models.pieces.hoplite import Hoplite
from aow.models.pieces.knight import Knight
from aow.models.pieces.pawn import Pawn
from aow.models.pieces.queen import Queen
from aow.models.pieces.rook import Rook
from aow.models.pieces.war_elephant import Warelephant
from aow.models.pieces.winged_knight import Wingedknight
from aow.utils.cell import CellUtils


class Check:
    def __init__(self, board):
        self.aow_board = board

    def is_check(self, king_pos: Cell, turn: int) -> bool:
        king_pos = CellUtils.make_cell(king_pos)

        diagonal_pieces = (Bishop, Queen)
        straight_pieces = (Rook, Queen, Warelephant)

        if self.is_check_diagonals(king_pos, diagonal_pieces, turn):
            return True

        if self.is_check_horizontal(king_pos, straight_pieces, turn):
            return True

        if self.is_check_verticals(king_pos, straight_pieces, turn):
            return True

        if self.is_check_knight(king_pos, turn):
            return True

        if self.is_check_winged_knight(king_pos, turn):
            return True

        return False

    def is_check_horizontal(self, king_pos: Cell, pieces_to_check: tuple, turn: int) -> bool:
        if self.is_check_left(king_pos, pieces_to_check, turn):
            return True

        if self.is_check_right(king_pos, pieces_to_check, turn):
            return True

        return False

    def is_check_left(self, king_pos: Cell, pieces_to_check: tuple, turn: int) -> bool:
        for c in range(king_pos.col - 1, -1, -1):
            if self.aow_board.is_tile_empty_on_both_side(Cell(king_pos.row, c), turn):
                continue
            p = self.aow_board.get_piece(Cell(7 - king_pos.row, c), 1 - turn)
            if isinstance(p, pieces_to_check):
                return True
            break
        return False

    def is_check_right(self, king_pos: Cell, pieces_to_check: tuple, turn: int) -> bool:
        for c in range(king_pos.col + 1, 8):
            if self.aow_board.is_tile_empty_on_both_side(Cell(king_pos.row, c), turn):
                continue
            p = self.aow_board.get_piece(Cell(7 - king_pos.row, c), 1 - turn)
            if isinstance(p, pieces_to_check):
                return True
            break
        return False

    def is_check_verticals(self, king_pos: Cell, pieces_to_check: tuple, turn: int) -> bool:
        if self.is_check_vertical(king_pos, pieces_to_check, turn, 1):
            return True

        if self.is_check_vertical(king_pos, pieces_to_check, turn, -1):
            return True

        return False

    def is_check_vertical(self, king_pos: Cell, pieces_to_check: tuple, turn: int, direction: int) -> bool:
        start, end, step = (king_pos.row + 1, 8, 1) if direction == 1 else (king_pos.row - 1, -1, -1)
        for r in range(start, end, step):
            d = r - king_pos.row
            if self.aow_board.is_tile_empty_on_both_side(Cell(r, king_pos.col), turn):
                continue
            p = self.aow_board.get_piece(Cell(7 - r, king_pos.col), 1 - turn)
            if isinstance(p, pieces_to_check):
                return True

            if d == 1 and isinstance(p, Hoplite):
                return True
            break
        return False

    def is_check_diagonals(self, king_pos: Cell, pieces_to_check: tuple, turn: int) -> bool:
        return (self.is_check_diagonal_down(king_pos, pieces_to_check, turn) or
                self.is_check_diagonal_up(king_pos, pieces_to_check, turn))

    def is_check_diagonal_up(self, king_pos: Cell, pieces_to_check: tuple, turn: int) -> bool:
        return (self.is_check_diagonal_up_right(king_pos, pieces_to_check, turn) or
                self.is_check_diagonal_up_left(king_pos, pieces_to_check, turn))

    def is_check_diagonal_down(self, king_pos: Cell, pieces_to_check: tuple, turn: int) -> bool:
        return (self.is_check_diagonal_down_right(king_pos, pieces_to_check, turn) or
                self.is_check_diagonal_down_left(king_pos, pieces_to_check, turn))

    def is_check_diagonal_up_right(self, king_pos: Cell, pieces_to_check: tuple, turn: int) -> bool:
        for r in range(king_pos.row - 1, -1, -1):
            d = r - king_pos.row
            if not self.aow_board.is_in_range(Cell(r, king_pos.col + d)):
                break

            if self.aow_board.is_tile_empty_on_both_side(Cell(r, king_pos.col + d), turn):
                continue

            p = self.aow_board.get_piece(Cell(7 - r, king_pos.col + d), 1 - turn)

            if isinstance(p, pieces_to_check):
                return True

            if d == 1 and (isinstance(p, Pawn) or isinstance(p, Hoplite)):
                return True

            break
        return False

    def is_check_diagonal_up_left(self, king_pos: Cell, pieces_to_check: tuple, turn: int) -> bool:
        for r in range(king_pos.row - 1, -1, -1):
            d = r - king_pos.row
            if not self.aow_board.is_in_range(Cell(r, king_pos.col - d)):
                break

            if self.aow_board.is_tile_empty_on_both_side(Cell(r, king_pos.col - d), turn):
                continue

            p = self.aow_board.get_piece(Cell(7 - r, king_pos.col - d), 1 - turn)

            if isinstance(p, pieces_to_check):
                return True

            if d == 1 and (isinstance(p, Pawn) or isinstance(p, Hoplite)):
                return True

            break
        return False

    def is_check_diagonal_down_right(self, king_pos: Cell, pieces_to_check: tuple, turn: int) -> bool:
        for r in range(king_pos.row + 1, 8):
            d = r - king_pos.row
            if not self.aow_board.is_in_range(Cell(r, king_pos.col + d)):
                break

            if self.aow_board.is_tile_empty_on_both_side(Cell(r, king_pos.col + d), turn):
                continue

            p = self.aow_board.get_piece(Cell(7 - r, king_pos.col + d), 1 - turn)

            if isinstance(p, pieces_to_check):
                return True

            if d == 1 and (isinstance(p, Pawn) or isinstance(p, Hoplite)):
                return True
            break
        return False

    def is_check_diagonal_down_left(self, king_pos: Cell, pieces_to_check: tuple, turn: int) -> bool:
        for r in range(king_pos.row + 1, 8):
            d = r - king_pos.row
            if not self.aow_board.is_in_range(Cell(r, king_pos.col - d)):
                break

            if self.aow_board.is_tile_empty_on_both_side(Cell(r, king_pos.col - d), turn):
                continue

            p = self.aow_board.get_piece(Cell(7 - r, king_pos.col - d), 1 - turn)

            if isinstance(p, pieces_to_check):
                return True

            if d == 1 and (isinstance(p, Pawn) or isinstance(p, Hoplite)):
                return True

            break
        return False

    def is_check_knight(self, king_pos: Cell, turn: int) -> bool:
        # KNIGHTS
        for r, c in Knight().get_moves():
            nr, nc = king_pos.row + r, king_pos.col + c
            if not self.aow_board.is_in_range(Cell(nr, nc)):
                continue
            if self.aow_board.is_piece(1 - turn, Cell(7 - nr, nc), Knight()):
                return True
        return False

    def is_check_winged_knight(self, king_pos: Cell, turn: int) -> bool:
        # WINGED KNIGHTS
        for r, c in Wingedknight().get_moves():
            nr, nc = king_pos.row + r, king_pos.col + c
            if not self.aow_board.is_in_range(Cell(nr, nc)):
                continue
            if self.aow_board.is_piece(1 - turn, Cell(7 - nr, nc), Wingedknight()):
                return True
        return False
