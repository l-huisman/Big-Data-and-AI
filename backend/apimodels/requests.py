from pydantic import BaseModel


class MoveRequest(BaseModel):
    move: str
    turn: int
    board: list
