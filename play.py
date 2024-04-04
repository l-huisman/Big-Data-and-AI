import pygame

from agents import PPOChess
from buffer.episode import Episode
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
white_ppo_path = 'results/DoubleAgents/white_ppo_dict.pt'
black_ppo_path = 'results/DoubleAgents/black_ppo_dict.pt'

ppo = PPO(
    env,
    hidden_layers=(2048,) * 4,
    epochs=100,
    buffer_size=32 * 2,
    batch_size=128,
)

# Create an instance of PPOChess
ppo_chess = PPOChess(env, ppo, 1, 32, "", white_ppo_path, black_ppo_path)

ep = Episode()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key != pygame.K_ESCAPE:
                running = False
                continue
    turn = env.turn
    if turn == 0:
        action_str = input("Choose action (e.g., 'e2e4'): ")

        if action_str == 'q':
            break

        # Convert human-readable action to chess move object
        try:
            f1 = int(action_str[1]) - 1
            f2 = ord(action_str[0]) - ord('a')
            from_pos = np.array([f1, f2])
            t1 = int(action_str[3]) - 1
            t2 = ord(action_str[2]) - ord('a')
            to_pos = np.array([t1, t2])

            src, dst, mask = env.get_all_actions(turn)
            action = np.where((src == from_pos).all(axis=1) & (dst == to_pos).all(axis=1))[0]

            print(f"Action = {action}", src[action], dst[action])
            action = action[0]
            rewards, done, infos = env.step(action)
            print(f"Rewards = {rewards}")
            print(f"Infos = {infos}")
            print("-" * 64)
        except:
            print("Invalid action")
            continue

        env.render()
        action_str = ''
    else:
        print("White" if turn else "Black")
        done, _ = ppo_chess.take_action(turn, ep)

        rewards = ep.rewards
        print("turn: ", env.turn)
        print(f"Rewards = {rewards}")
        print("-" * 64)
        env.render()
    if done:
        env.reset()
        print("RESET")


env.close()