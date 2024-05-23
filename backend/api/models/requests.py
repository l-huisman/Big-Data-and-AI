from pydantic import BaseModel


class AIGameRequest(BaseModel):
    white_model: str
    black_model: str


class MoveRequest(BaseModel):
    move: str
    turn: int
    board: list
    resources: list


class ActionRequest(BaseModel):
    board: list
    turn: int
    pieceLocation: str
