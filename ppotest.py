import pygame
from agents import PPOChess
from chess import Chess
from time import sleep
import numpy as np
import random
import sys

from learnings.ppo import PPO

sys.setrecursionlimit(300)
env = Chess(window_size=800)
env.render()

# Paths to your trained models
white_ppo_path = 'results/DoubleAgents/white_ppo.pt'
black_ppo_path = 'results/DoubleAgents/black_ppo.pt'

ppo = PPO(
    env,
    hidden_layers=(2048,) * 4,
    epochs=100,
    buffer_size=32 * 2,
    batch_size=128,
)

# Create an instance of PPOChess
chess_game = PPOChess(env, ppo, 0, 0, "", white_ppo_path, black_ppo_path)

# Play the game
while True:
    done, _ = chess_game.take_action(chess_game.env.turn, None)
    env.render()
    sleep(1)  # Pause for a short time to make the game viewable
    if done:
        break