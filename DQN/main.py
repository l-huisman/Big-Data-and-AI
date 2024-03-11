# https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
import os
import torch
import gymnasium as gym
from visualisation import plot_durations
from itertools import count
from agent import DQNAgent
from net import DQN

PATH = "agents/DQN.pth"


def initialise_environment():
    env = gym.make("CartPole-v1")
    n_actions = env.action_space.n
    state, _ = env.reset()
    n_observations = len(state)
    return env, n_actions, n_observations


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    environment, n_actions, n_observations = initialise_environment()

    policy_net = DQN(n_observations, n_actions).to(device)
    target_net = DQN(n_observations, n_actions).to(device)
    if os.path.exists(PATH):
        target_net.load_state_dict(torch.load(PATH))

    agent = DQNAgent(policy_net, target_net, device, environment)

    episode_durations = []
    num_episodes = 1200 if torch.cuda.is_available() else 400

    for i_episode in range(num_episodes):
        state = environment.reset()
        for t in count():
            action = agent.select_action(state)
            observation, reward, terminated, truncated, _ = environment.step(
                action.item()
            )
            reward = torch.tensor([reward], device=device)
            done = terminated or truncated
            next_state = (
                None
                if terminated
                else torch.tensor(
                    observation, dtype=torch.float32, device=device
                ).unsqueeze(0)
            )

            agent.memory.push(state, action, next_state, reward)
            agent.optimize_model()
            agent.soft_update()

            if done:
                episode_durations.append(t + 1)
                plot_durations(episode_durations)
                break


if __name__ == "__main__":
    main()
