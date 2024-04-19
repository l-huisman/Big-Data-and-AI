from fastapi import FastAPI, HTTPException

from learnings.ppo import PPO
from learnings.dqn import DQNLearner
from apimodels.requests import MoveRequest
from apimodels.responses import MoveResponse
from agents import PPOChess
from buffer.episode import Episode
from chess import Chess
import numpy as np
import sys

app = FastAPI()

sys.setrecursionlimit(300)
env = Chess(window_size=800)

white_ppo_path = 'results/DoubleAgentsPPO/white_dict.pt'
black_ppo_path = 'results/DoubleAgentsPPO/black_dict.pt'

white_dqn_path = 'results/DoubleAgentsDQN/white_dict.pt'
black_dqn_path = 'results/DoubleAgentsDQN/black_dict.pt'

ppo = PPO(
    env,
    hidden_layers=(2048,) * 4,
    epochs=100,
    buffer_size=32 * 2,
    batch_size=128,
)

ppo_chess: PPOChess
episode: Episode


@app.get("/initialize", status_code=201)
def initialize():
    global ppo_chess, episode
    try:
        env.reset()
        ppo_chess = PPOChess(env, ppo, 1, 32, "", white_ppo_path, black_ppo_path)
        episode = Episode()
        return {"message": "Started new game successfully."}
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Could not find model, maybe no model has been trained yet.")


@app.post("/move")
def move(move_request: MoveRequest):
    global ppo_chess, episode
    if ppo_chess or episode is None:
        raise HTTPException(status_code=404, detail="No game has been initialized yet.")
    action_str = move_request.move
    move_response = MoveResponse()
    if action_str == 'q':
        return {"message": "Game has ended."}
    try:
        f1 = int(action_str[1]) - 1
        f2 = ord(action_str[0]) - ord('a')
        from_pos = np.array([f1, f2])
        f1 = int(action_str[3]) - 1
        f2 = ord(action_str[2]) - ord('a')
        to_pos = np.array([f1, f2])

        src, dst, mask = env.get_all_actions(env.turn)
        action = np.where((src == from_pos).all(axis=1) & (dst == to_pos).all(axis=1))[0]
        if len(action) == 0:
            raise Exception("Invalid move.")

        env.step(action[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid move.")

    try:
        done, _ = ppo_chess.take_action(env.turn, episode)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while taking action.")

    move_response.board = env.board
    move_response.cards = {}
    move_response.resources = 0
    move_response.has_game_ended = done

    return move_response
