import numpy as np
from fastapi import HTTPException

from api.models.requests import MoveRequest
from api.models.responses import MoveResponse
from api.routes.base import BaseRoute
from utils import (
    reverse_move,
    convert_move_to_positions,
)

MOVE_REGEX = r"^[a-h][1-8][a-h][1-8]$"


class Move(BaseRoute):
    def __init__(self, env, agent, episode, move_request: MoveRequest):
        super().__init__(env)
        self.agent = agent
        self.episode = episode
        self.move_request = move_request

    def execute(self) -> MoveResponse:
        self.logger.info(f"Received move request: {self.move_request}")
        self.reset_environment()

        if self.agent is None:
            self.logger.error("No game has been initialized yet.")
            self.raise_http_exception(404, "No game has been initialized yet.")

        board = self.convert_board(self.move_request.board)
        self.validate_board_size(board)

        self.env.resources = self.move_request.resources
        self.env.set_board(board)
        self.env.turn = self.move_request.turn
        action_str = self.move_request.move

        self.validate_move_format(action_str)

        player_move_board, done = self.process_player_move(action_str)

        if done:
            return MoveResponse(
                playerMoveBoard=player_move_board,
                CombinedMoveBoard=player_move_board,
                cards=[],
                resources=self.env.resources, has_game_ended=done
            )

        self.process_ai_move(turn=self.env.turn, episode=self.episode)
        self.logger.info("Move processed successfully.")
        return MoveResponse(playerMoveBoard=player_move_board, CombinedMoveBoard=self.env.board.tolist(), cards=[],
                            resources=self.env.resources,
                            has_game_ended=self.env.done)

    def process_ai_move(self, turn, episode):
        try:
            self.agent.take_action(turn, episode)
        except Exception as e:
            self.logger.error(f"An error occurred while processing the AI's move. {e}")
            self.raise_http_exception(status_code=500, detail="An error occurred while processing the AI's move.")

    def convert_board(self, board) -> np.ndarray:
        try:
            board = np.array(board)
            if not board.any():
                self.raise_http_exception(400, "Please provide a board.")
        except Exception as e:
            self.logger.warning(f"An error occurred while processing the board. {e}")
            self.raise_http_exception(400, "Invalid board.")
        return board

    def validate_move_format(self, action_str) -> None:
        self.validate_regex(string=action_str, regex=MOVE_REGEX,
                            http_response_message="Move does not have the correct format."
                                                  " Please provide a move in the format of \"a1a2\".")

    def process_player_move(self, action_str) -> (np.ndarray, bool):
        try:
            if self.env.turn == 1:
                action_str = reverse_move(action_str)

            from_pos, to_pos = convert_move_to_positions(action_str)
            src, dst, _ = self.env.get_all_actions(self.env.turn)
            action = np.nonzero((src == from_pos).all(axis=1) & (dst == to_pos).all(axis=1))[0]
            if len(action) == 0:
                self.raise_http_exception(400, "Invalid move.")
            _, done, _ = self.env.step(int(action[0]))

            player_move_board = self.env.board.tolist()
            return player_move_board, done
        except HTTPException as e:
            raise e
        except Exception as e:
            self.logger.error("Something went wrong while processing the move. " + str(e))
            self.raise_http_exception(400, "Invalid move")
