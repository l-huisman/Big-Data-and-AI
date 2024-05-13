from api.routes.base import BaseRoute


class AiGame(BaseRoute):
    def __init__(self, env, agent, episode, ai_game_request):
        super().__init__(env)
        self.agent = agent
        self.episode = episode
        self.ai_game_request = ai_game_request

    def execute(self):
        self.logger.info(f"Received aigame request: {ai_game_request}")
        response = AIGameResponse(game=[], statistics=[])
        try:
            env.reset()

            match ai_game_request.white_model.capitalize():
                case "PPO":
                    white_model = WHITE_PPO_PATH
                case "DQN":
                    # white_model = WHITE_DQN_PATH
                    self.logger.info("DQN not implemented yet, using PPO instead.")
                    white_model = WHITE_PPO_PATH
                case _:
                    white_model = WHITE_PPO_PATH

            match ai_game_request.black_model.capitalize():
                case "PPO":
                    black_model = BLACK_PPO_PATH
                case "DQN":
                    # black_model = BLACK_DQN_PATH
                    self.logger.info("DQN not implemented yet, using PPO instead.")
                    black_model = BLACK_PPO_PATH
                case _:
                    black_model = BLACK_PPO_PATH

            ppo_chess = PPOChess(env, ppo, 1, 32, "", white_model, black_model)
            episode = Episode()
            self.logger.info("Initialized AI game.")

            # Play the game
            counter = 0
            response.game.append(ppo_chess.env.board.tolist())
            response.statistics.append({"rewards": [0, 0], "infos": [[], []], "end": False})

            while True:
                done, _ = ppo_chess.take_action(ppo_chess.env.turn, episode)
                response.statistics.append({"rewards": _[1], "infos": _[7], "end": done})
                response.game.append(ppo_chess.env.board.tolist())

                counter += 1
                if done:
                    self.logger.info("Game Over")
                    self.logger.info("Winner: White" if ppo_chess.env.turn else "Winner: Black")
                    self.logger.info("Game Length: ", counter)
                    break

            self.logger.info(f"AI game completed.")
            return response
        except FileNotFoundError as e:
            self.logger.error(f"Could not find model on specified location, make sure the location is correct. {e}")
            raise HTTPException(status_code=500, detail="Could not find any model.")
        except Exception as e:
            self.logger.error(f"An error occurred while resetting the game. {e}")
            raise HTTPException(status_code=500, detail="An error occurred while initializing the game.")
