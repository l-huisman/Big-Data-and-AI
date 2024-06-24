import os
from copy import deepcopy

import torch

from aow.game.aow import ArtOfWar
from buffer.episode import Episode
from learnings.base import Learning
from .base import BaseAgent


class DoubleAgents(BaseAgent):
    def __init__(
            self,
            env: ArtOfWar,
            learner: Learning,
            episodes: int,
            train_on: int,
            result_folder: str,
    ) -> None:
        super().__init__(env, learner, episodes, train_on, result_folder)
        self.white_agent = deepcopy(learner)
        self.black_agent = deepcopy(learner)

    def add_episodes(self, white: Episode, black: Episode) -> None:
        self.white_agent.remember(white)
        self.black_agent.remember(black)

    def learn(self):
        self.white_agent.learn()
        self.black_agent.learn()

    def save_learners(self):
        if not os.path.exists(self.result_folder):
            os.makedirs(self.result_folder)

        self.white_agent.save(self.result_folder, "white")
        self.black_agent.save(self.result_folder, "black")
        torch.save(self.white_agent.state_dict(), f"{self.result_folder}/white_dict.pt")
        torch.save(self.black_agent.state_dict(), f"{self.result_folder}/black_dict.pt")
