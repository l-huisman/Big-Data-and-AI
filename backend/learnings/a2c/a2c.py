import os
import gym
import numpy as np
import torch as T
import torch.optim as optim

from tqdm import tqdm
from buffer.a2c import BufferPPO
from buffer.episode import Episode

from learnings.base import Learning
from learnings.a2c.actor import Actor
from learnings.a2c.critic import Critic


class A2C(Learning):
    def __init__(self, config):
        super(A2C, self).__init__(config)

        self.env = gym.make(config.env_name)
        self.env.seed(config.seed)
        self.config = config

        self.actor = Actor(config)
        self.critic = Critic(config)

        self.buffer = BufferPPO(config)

        self.actor_optim = optim.Adam(self.actor.parameters(), lr=config.actor_lr)
        self.critic_optim = optim.Adam(self.critic.parameters(), lr=config.critic_lr)

        self.total_steps = 0
        self.total_episodes = 0
        self.total_updates = 0

    def learn(self):
        while self.total_steps < self.config.max_steps:
            self.learn_episode()
            self.total_episodes += 1

    def learn_episode(self):
        episode = Episode(self.env, self.actor, self.critic, self.buffer, self.config)
        episode.learn()

        self.total_steps += episode.total_steps
        self.total_updates += episode.total_updates

        self.actor_optim.zero_grad()
        self.critic_optim.zero_grad()

        self.buffer.compute_returns(self.critic)
        self.buffer.compute_advantages(self.critic)

        self.actor_loss = self.buffer.compute_actor_loss(self.actor)
        self.critic_loss = self.buffer.compute_critic_loss(self.critic)

        self.actor_loss.backward()
        self.critic_loss.backward()

        self.actor_optim.step()
        self.critic_optim.step()

        self.buffer.clear()

        self.log()

    def log(self):
        if self.total_episodes % self.config.log_interval == 0:
            print(f"Episode: {self.total_episodes}, Total Steps: {self.total_steps}, Total Updates: {self.total_updates}, Actor Loss: {self.actor_loss.item()}, Critic Loss: {self.critic_loss.item()}")

    def save(self):
        T.save(self.actor.state_dict(), os.path.join(self.config.save_dir, "actor.pth"))
        T.save(self.critic.state_dict(), os.path.join(self.config.save_dir, "critic.pth"))

    def load(self):
        self.actor.load_state_dict(T.load(os.path.join(self.config.save_dir, "actor.pth")))
        self.critic.load_state_dict(T.load(os.path.join(self.config.save_dir, "critic.pth")))