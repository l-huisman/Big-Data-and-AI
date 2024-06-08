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
        self.validate_resources(self.move_request.resources)

        self.env.aow_board.resources = self.move_request.resources
        self.env.aow_board.set_board(board)
        self.env.aow_logic.turn = self.move_request.turn
        action_str = self.move_request.move

        self.validate_move_format(action_str)

        player_move_board, done = self.process_player_move(action_str)

        if done:
            return MoveResponse(
                playerMoveBoard=player_move_board,
                combinedMoveBoard=player_move_board,
                cards=[],
                resources=self.env.aow_board.resources, has_game_ended=done
            )

        while self.env.aow_logic.turn != self.move_request.turn:
            self.process_ai_move(turn=self.env.aow_logic.turn, episode=self.episode)

        self.logger.info("Move processed successfully.")
        return MoveResponse(playerMoveBoard=player_move_board,
                            combinedMoveBoard=self.env.aow_board.get_numeric_board().tolist(),
                            cards=[],
                            resources=self.env.aow_board.resources,
                            has_game_ended=self.env.aow_logic.done)

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
            if self.env.aow_logic.turn == 1:
                action_str = reverse_move(action_str)

            from_pos, to_pos = convert_move_to_positions(action_str)
            src, dst, mask = self.env.aow_logic.get_all_actions(self.env.aow_logic.turn)
            valid_src, valid_dst, valid_indices = self.get_valid_actions(src, dst, mask)
            index = np.nonzero((valid_src == from_pos).all(axis=1) & (valid_dst == to_pos).all(axis=1))[0]
            action = valid_indices[index] if len(index) > 0 else []
            if len(action) == 0:
                self.raise_http_exception(400, "Invalid move.")
            _, done, _ = self.env.step(int(action))

            player_move_board = self.env.aow_board.get_numeric_board().tolist()
            return player_move_board, done
        except HTTPException as e:
            raise e
        except Exception as e:
            self.logger.error("Something went wrong while processing the move. " + str(e))
            self.raise_http_exception(400, "Invalid move")

    @staticmethod
    def get_valid_actions(src, dst, mask):
        src = np.array(src)
        dst = np.array(dst)
        mask = np.array(mask)

        if len(src) != len(dst):
            raise ValueError("All input arrays must have the same length")

        valid_indices = np.nonzero(mask == 1)[0]
        valid_src = src[valid_indices]
        valid_dst = dst[valid_indices]

        print("Possible actions: 2")

        # print all valid actions
        for i in valid_indices:
            to_loc = dst[i]
            from_loc = src[i]
            string_to = chr(to_loc[1] + ord('a')) + str(to_loc[0] + 1)
            string_from = chr(from_loc[1] + ord('a')) + str(from_loc[0] + 1)
            print(f"{src[i]} -> {dst[i]} or {string_from} -> {string_to}")

        return valid_src, valid_dst, valid_indices

    def validate_resources(self, resources):
        if len(resources) != 2:
            self.raise_http_exception(400, "Invalid resources. Please provide resources in the format of [n, n].")
        if not all(isinstance(i, int) for i in resources):
            self.raise_http_exception(400, "Invalid resources. Please provide resources in the format of [n, n].")
