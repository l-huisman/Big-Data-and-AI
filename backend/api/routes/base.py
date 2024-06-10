import logging

from fastapi import HTTPException

from learnings.ppo import PPO
from utils import matches_regex

BOARD_LENGTH = 8
BOARD_WIDTH = 8
BOARD_SIDES = 2


class BaseRoute:
    def __init__(self, env):
        self.logger = logging.getLogger(__name__)
        self.env = env

    WHITE_PPO_PATH = 'results/DoubleAgentsPPO/white_dict.pt'
    BLACK_PPO_PATH = 'results/DoubleAgentsPPO/black_dict.pt'
    WHITE_DQN_PATH = 'results/DoubleAgentsDQN/white_dict.pt'
    BLACK_DQN_PATH = 'results/DoubleAgentsDQN/black_dict.pt'
    WHITE_A2C_PATH = 'results/DoubleAgentsA2C/white_dict.pt'
    BLACK_A2C_PATH = 'results/DoubleAgentsA2C/black_dict.pt'

    def execute(self):
        raise NotImplementedError()

    def validate_regex(self, string, regex, http_response_message) -> None:
        if not matches_regex(string, regex):
            self.raise_http_exception(status_code=400, detail=http_response_message)

    @staticmethod
    def raise_http_exception(status_code, detail):
        raise HTTPException(status_code=status_code, detail=detail)

    def validate_board_size(self, board):
        if len(board) != BOARD_SIDES:
            self.raise_http_exception(400, f"Invalid board size. ({len(board)}) should be {BOARD_SIDES}.")
        if len(board[0]) != BOARD_WIDTH or len(board[1]) != BOARD_WIDTH:
            self.raise_http_exception(400,
                                      f"Invalid board size. ({len(board[0])}, {len(board[1])}) should be {BOARD_WIDTH},"
                                      f" {BOARD_WIDTH}")
        for row in board[0]:
            if len(row) != BOARD_LENGTH:
                self.raise_http_exception(400, f"Invalid board size. ({len(row)}) should be {BOARD_LENGTH}")
        for row in board[1]:
            if len(row) != BOARD_LENGTH:
                self.raise_http_exception(400, f"Invalid board size. ({len(row)}) should be {BOARD_LENGTH}")

    def reset_environment(self):
        try:
            self.env.reset()
        except Exception as e:
            self.logger.error(f"An error occurred while resetting the game. {e}")
            raise self.raise_http_exception(500, detail="An error occurred while resetting the game.")

    def get_ppo(self):
        return PPO(
            self.env,
            hidden_layers=(2048,) * 4,
            epochs=100,
            buffer_size=32 * 2,
            batch_size=128,
        )
