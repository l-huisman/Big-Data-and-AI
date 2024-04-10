import gym
import numpy as np
import torch as T
from tqdm import tqdm

from buffer.dqn import BufferDQN
from buffer.episode import Episode
from learnings.base import Learning
from learnings.dqn.dqn import DQN


class DQNLearner(Learning):
    def __init__(
            self,
            environment: gym.Env,
            epochs: int,
            gamma: float,
            learning_rate: float,
            hidden_layers: tuple[int],
            buffer_size: int,
            batch_size: int,
            epsilon: float,
            epsilon_decay: float,
            epsilon_min: float,
            tau: float,
            update_every: int
    ) -> None:
        super().__init__(environment, epochs, gamma, learning_rate)
        self.hidden_layers = hidden_layers
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.tau = tau
        self.update_every = update_every

        self.buffer = BufferDQN(
            max_size=buffer_size,
            batch_size=batch_size,
            gamma=gamma,
            tau=tau
        )

        self.dqn = DQN(self.state_dim, self.action_dim, hidden_layers)
        self.optimizer = T.optim.Adam(self.dqn.parameters(), lr=learning_rate)

        self.to(self.device)

    def take_action(self, state: np.array, action_mask: np.array):
        state = T.Tensor(state).unsqueeze(0).to(self.device)
        action_mask = T.Tensor(action_mask).unsqueeze(0).to(self.device)
        action_values = self.dqn(state)
        action_values = action_values * action_mask
        # these two might not work
        probs = T.nn.functional.softmax(action_values, dim=1)
        value = T.max(action_values).item()

        action = T.argmax(action_values).item()
        return action, probs, value

    def epoch(self):
        if len(self.buffer) < self.batch_size:
            return

        for _ in range(self.update_every):
            states, actions, rewards, next_states, dones = self.buffer.sample(self.batch_size)

            states = T.Tensor(states).to(self.device)
            actions = T.Tensor(actions).to(self.device)
            rewards = T.Tensor(rewards).to(self.device)
            next_states = T.Tensor(next_states).to(self.device)
            dones = T.Tensor(dones).to(self.device)

            curr_Q = self.dqn(states).gather(1, actions.unsqueeze(-1)).squeeze(-1)
            next_Q = self.dqn(next_states).max(dim=1)[0]
            target_Q = rewards + (self.gamma * next_Q * (1 - dones))

            loss = F.mse_loss(curr_Q, target_Q.detach())
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def learn(self):
        for _ in tqdm(range(self.epochs), desc="DQN Learning", ncols=64, leave=False):
            self.epoch()
        self.buffer.clear()

    def remember(self, episode: Episode):
        self.buffer.add(episode)

    def save(self, folder: str, name: str = "dqn"):
        T.save(self.dqn.state_dict(), f"{folder}/{name}.pt")
