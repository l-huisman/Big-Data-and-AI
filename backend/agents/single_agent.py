from buffer.episode import Episode
from chess.game.aow import ArtOfWar
from learnings.base import Learning
from .base import BaseAgent


class SingleAgentChess(BaseAgent):
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
        self.learner.save(self.result_folder, "single_agent_ppo.pt")
