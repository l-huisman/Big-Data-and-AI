import os

import torch

from aow.game.aow import ArtOfWar
from buffer.episode import Episode
from learnings.base import Learning
from .base import BaseAgent


class SingleAgent(BaseAgent):
    def __init__(
            self,
            env: ArtOfWar,
            learner: Learning,
            episodes: int,
            train_on: int,
            result_folder: str,
    ) -> None:
        super().__init__(env, learner, episodes, train_on, result_folder)

    def add_episodes(self, white: Episode, black: Episode) -> None:
        self.learner.remember(white)
        self.learner.remember(black)

    def learn(self):
        self.learner.learn()

    def save_learners(self):
        if not os.path.exists(self.result_folder):
            os.makedirs(self.result_folder)

        self.learner.save(self.result_folder, "single_agent.pt")
        torch.save(self.learner.state_dict(), f"{self.result_folder}/single_agent_dict.pt")
