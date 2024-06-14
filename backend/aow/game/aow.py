from typing import Union, Optional, List

import gym
from gym.core import RenderFrame

import aow.constants.rewards as Rewards
from aow.game.aow_logic import AoWLogic
from aow.models.board import AoWBoard
from aow.models.cards import DutchWaterline
from aow.models.types import Cell
from aow.utils.pygame import PyGameUtils


class ArtOfWar(gym.Env):
    def __init__(self, max_steps: int = 128, window_size: int = 800, render_mode: str = 'human',
                 console_render: bool = False):
        self.aow_board = AoWBoard()
        self.pygame_utils = PyGameUtils(window_size=window_size, render_mode=render_mode)
        self.aow_logic = AoWLogic(max_steps=max_steps, board=self.aow_board)
        self.console_render = console_render

    def step(self, action: int) -> tuple[list[int], bool, list[set]]:
        assert not self.aow_logic.is_game_done(), "the game is finished reset"
        assert action < self.aow_logic.action_space_length, f"action number must be less than {self.aow_logic.action_space_length}."

        source_pos, possibles, actions_mask = self.aow_logic.get_all_actions(self.aow_logic.turn)
        assert actions_mask[action], f"Cannot Take This Action = {action}, {source_pos[action]} -> {possibles[action]}"

        from_pos = Cell(int(source_pos[action][0]), int(source_pos[action][1]))
        next_pos = Cell(int(possibles[action][0]), int(possibles[action][1]))

        if self.console_render is True:
            print(self.aow_board.get_numeric_board())
            print(f"Action = {action}, {from_pos} -> {next_pos}")

        rewards, infos, end_turn = self.handle_moves(from_pos, next_pos)

        rewards, infos = self.update_game_state(rewards, infos)

        if from_pos != next_pos or end_turn:
            if not end_turn:
                self.aow_logic.turn = self.aow_logic.turn
            else:
                self.aow_board.add_resources(self.aow_logic.turn, 1)
                self.aow_logic.turn = 1 - self.aow_logic.turn
        self.aow_logic.steps += 1
        return rewards, self.aow_logic.is_game_done(), infos

    def handle_moves(self, from_pos: Cell, next_pos: Cell) -> tuple[list[int], list[set], bool]:
        if from_pos == next_pos and self.aow_board.get_piece(from_pos, self.aow_logic.turn).is_upgradable():
            return self.handle_same_position(from_pos)
        elif ((from_pos == (2, 0) or from_pos == (3, 0) or from_pos == (4, 0) or from_pos == (5, 0))
              and next_pos == Cell(0, 7)):
            return self.handle_dutch_waterline(from_pos)
        else:
            return self.handle_move_piece(from_pos, next_pos)

    def handle_same_position(self, from_pos: Cell) -> tuple[list[int], list[set], bool]:
        source_pos_piece = self.aow_board.get_piece(Cell(from_pos[0], from_pos[1]), self.aow_logic.turn)
        rewards, infos = self.aow_logic.upgrade_piece(from_pos, self.aow_logic.turn, source_pos_piece)
        end_turn = False
        return rewards, infos, end_turn

    def handle_dutch_waterline(self, from_pos: Cell) -> tuple[list[int], list[set], bool]:
        card: DutchWaterline | None = self.aow_board.get_card(turn=self.aow_logic.turn, card=DutchWaterline())
        assert card is not None, "Dutch Waterline card not found"
        card.play(from_pos, self.aow_board, self.aow_logic.turn)

        rewards = self.aow_logic.add_reward(reward=Rewards.DUTCH_WATERLINE, turn=self.aow_logic.turn)
        infos = [set(), set()]
        end_turn = False
        return rewards, infos, end_turn

    def handle_move_piece(self, from_pos: Cell, next_pos: Cell) -> tuple[list[int], list[set], bool]:
        rewards, infos = self.aow_logic.move_piece(from_pos, next_pos, self.aow_logic.turn, temp=False)
        end_turn = True
        return rewards, infos, end_turn

    def update_game_state(self, rewards: list[int], infos: list[set]) -> tuple[list[int], list[set]]:
        rewards, infos = self.aow_logic.update_checks(rewards, infos)
        rewards, infos = self.aow_logic.update_check_mates(rewards, infos)
        rewards, infos = self.aow_logic.update_draw(rewards, infos)
        return rewards, infos

    def render(self) -> Optional[Union[RenderFrame, List[RenderFrame]]]:
        """
        Render the environment
        :return: Optional[Union[RenderFrame, List[RenderFrame]]]: The rendered frame
        """
        return self.pygame_utils.render(self.aow_board.get_numeric_board())

    def reset(self, **kwargs) -> None:
        """
        Reset the environment
        :param kwargs: dict: The arguments to reset the environment
        """
        self.aow_logic.done = False
        self.aow_logic.turn = 0  # 0 or 1, 0 means white, 1 means black
        self.aow_logic.steps = 0
        self.aow_logic.checked = [False, False]
        self.aow_board.reset()
