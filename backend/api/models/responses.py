from pydantic import BaseModel


class AIGameResponse(BaseModel):
    game: list
    statistics: list


class MoveResponse(BaseModel):
    playerMoveBoard: list
    CombinedMoveBoard: list
    cards: list
    resources: int
    has_game_ended: bool

class ActionResponse(BaseModel):
    possibleMoves: list

class InitializeResponse(BaseModel):
    board: list
    cards: list
    resources: int
