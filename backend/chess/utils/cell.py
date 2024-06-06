from chess.models import Cell


class CellUtils:
    @staticmethod
    def make_cell(pos: tuple[int, int] | Cell) -> Cell:
        """
        Make a cell from a tuple
        :param pos: tuple[int, int] | Cell: The position to make a cell from
        :return: Cell: The cell from the tuple
        """
        if not isinstance(pos, Cell):
            pos = Cell(pos[0], pos[1])
        return pos
