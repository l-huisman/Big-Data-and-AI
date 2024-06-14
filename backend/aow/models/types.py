import numpy as np
from typing import NamedTuple


class Cell(NamedTuple):
    row: int
    col: int


Action = tuple[Cell, Cell]
Trajectory = tuple[np.ndarray, float, bool, dict]
