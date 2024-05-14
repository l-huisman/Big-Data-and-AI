from pydantic import BaseModel


class AIGameResponse(BaseModel):
    game: list
    statistics: list


class MoveResponse(BaseModel):
    playerMoveBoard: list
    combinedMoveBoard: list
    cards: list
    resources: list
    has_game_ended: bool

class ActionResponse(BaseModel):
    possibleMoves: list

class InitializeResponse(BaseModel):
    board: list
    cards: list
    resources: list
