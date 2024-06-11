from pydantic import BaseModel


class AIGameResponse(BaseModel):
    game: list
    statistics: list
    source_pos: list
    possibles: list
    action_mask: list
    winner: str


class MoveResponse(BaseModel):
    playerMoveBoard: list
    combinedMoveBoard: list
    cards: list
    resources: list
    has_game_ended: bool
    infos: list


class ActionResponse(BaseModel):
    possibleMoves: list


class InitializeResponse(BaseModel):
    board: list
    cards: list
    resources: list
