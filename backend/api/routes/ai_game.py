from fastapi import HTTPException

from agents import PPOChess
from api.models.requests import AIGameRequest
from api.models.responses import AIGameResponse
from api.routes.base import BaseRoute
from buffer.episode import Episode


class AiGame(BaseRoute):
    def __init__(self, env, ai_game_request: AIGameRequest):
        super().__init__(env)
        self.ai_game_request = ai_game_request

    def execute(self):
        try:
            self.logger.info(f"Received aigame request: {self.ai_game_request}")
            self.reset_environment()
            agent = self.get_agent(black_model_name=self.ai_game_request.black_model,
                                   white_model_name=self.ai_game_request.white_model)
            return self.play_game(agent=agent, episode=Episode())
        except HTTPException as e:
            raise e
        except FileNotFoundError as e:
            self.logger.error(f"Could not find model on specified location, make sure the location is correct. {e}")
            raise self.raise_http_exception(status_code=500, detail="Could not find any model.")
        except Exception as e:
            self.logger.error(f"An error occurred while resetting the game. {e}")
            raise self.raise_http_exception(status_code=500, detail="An error occurred while initializing the game.")

    def get_agent(self, white_model_name: str = "PPO", black_model_name: str = "PPO"):
        match white_model_name.capitalize():
            case "PPO":
                white_model = self.WHITE_PPO_PATH
            case "DQN":
                # white_model = self.WHITE_DQN_PATH
                self.logger.info("DQN not implemented yet, using PPO instead.")
                white_model = self.WHITE_PPO_PATH
            case _:
                white_model = self.WHITE_PPO_PATH

        match black_model_name.capitalize():
            case "PPO":
                black_model = self.BLACK_PPO_PATH
            case "DQN":
                # black_model = BLACK_DQN_PATH
                self.logger.info("DQN not implemented yet, using PPO instead.")
                black_model = self.BLACK_PPO_PATH
            case _:
                black_model = self.BLACK_PPO_PATH

        return PPOChess(self.env, self.get_ppo(), 1, 32, "", white_model, black_model)

    def play_game(self, agent, episode) -> AIGameResponse:
        response = AIGameResponse(game=[], statistics=[])

        response.game.append(agent.env.board.tolist())
        response.statistics.append({"rewards": [0, 0], "infos": [[], []], "end": False})

        done = False
        while not done:
            done, _ = agent.take_action(agent.env.turn, episode)
            response.statistics.append({"rewards": _[1], "infos": _[7], "end": done})
            response.game.append(agent.env.board.tolist())

        self.logger.info("AI game completed.")
        return response
