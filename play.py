import pygame
from chess import Chess
from time import sleep
import numpy as np
import random
import sys

sys.setrecursionlimit(100)
env = Chess(window_size=800)
env.render()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key != pygame.K_SPACE:
        #         continue
        #     else:
    turn = env.turn
    if turn == 0:
        action_str = input("Choose action (e.g., 'e2e4'): ")
    
        # Convert human-readable action to chess move object
        try:
            action = Chess.Move.from_uci(action_str)
        except ValueError:
            print("Invalid action! Please choose a valid action in algebraic notation (e.g., 'e2e4').")
            continue  # Continue to prompt for action
        env.render()
    else:
        print("White" if turn else "Black")
        src, dst, mask = env.get_all_actions(turn)
        action = random.sample(list(np.where(mask == 1)[0]), 1)[0]
        rewards, done, infos = env.step(action)
        print(f"Rewards = {rewards}")
        print(f"Infos = {infos}")
        print("-" * 64)
        env.render()
    if done:
        env.reset()
        print("RESET")


env.close()