import numpy as np
from pydantic import BaseModel

class AIGameResponse(BaseModel):
    game: list
    statistics: list

class MoveResponse(BaseModel):
    board: list
    cards: list
    resources: int
    has_game_ended: bool


class InitializeResponse(BaseModel):
    board: list
    cards: list
    resources: int
