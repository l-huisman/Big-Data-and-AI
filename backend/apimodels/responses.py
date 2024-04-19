from pydantic import BaseModel


class MoveResponse(BaseModel):
    board: str
    cards: str
    resources: str
    has_game_ended: bool


class InitializeResponse(BaseModel):
    board: str
    cards: str
    resources: str
