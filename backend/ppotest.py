import pygame
from agents import PPOChess
from buffer.episode import Episode
from chess import Chess
from time import sleep
import numpy as np
import random
import sys

from learnings.dqn import DQNLearner
from learnings.ppo import PPO

sys.setrecursionlimit(300)
env = Chess(window_size=800)
env.render()

# Paths to your trained apimodels
white_ppo_path = 'results/DoubleAgentsPPO/white_dict.pt'
black_ppo_path = 'results/DoubleAgentsPPO/black_dict.pt'

ppo = PPO(
    env,
    hidden_layers=(2048,) * 4,
    epochs=100,
    buffer_size=32 * 2,
    batch_size=128,
)

# dqn = DQNLearner(
#     env,
#     epochs=100,
#     gamma=0.99,
#     learning_rate=0.003,
#     hidden_layers=(2048,) * 4,
#     buffer_size=32,
#     batch_size=128,
#     epsilon=0.1,
#     epsilon_decay=0.995,
#     epsilon_min=0.01,
#     tau=0.99,
#     update_every=4,
# )

# Create an instance of PPOChess
chess_game = PPOChess(env, ppo, 1, 32, "", white_ppo_path, black_ppo_path)

episode = Episode()
# Play the game
counter = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    done, _ = chess_game.take_action(chess_game.env.turn, episode)
    # print("turn: ", chess_game.env.turn)
    env.render()
    sleep(1)  # Pause for a short time to make the game viewable
    counter += 1
    if done:
        print("Game Over")
        print("Winner: White" if chess_game.env.turn else "Winner: Black")
        print("Game Length: ", counter)
        break
