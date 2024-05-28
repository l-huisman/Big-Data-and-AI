from typing import Union

import contants.colors as Colors
import contants.info_keys as InfoKeys
import chess.moves as Moves
import chess.pieces as Pieces
import chess.rewards as Rewards
import gym
import numpy as np
import pygame
from chess.types import Cell
from gym import spaces
from pygame.font import Font
from pygame.surface import Surface


class Chess(gym.Env):
    metadata: dict = {
        "render_mode": ("human", "rgb_array"),
    }

    def __init__(
            self,
            max_steps: int = 128,
            render_mode: str = "human",
            window_size: int = 800,
    ) -> None:
        self.action_space_length = 1200  # 3584
        self.action_space = spaces.Discrete(self.action_space_length)  # standard chess board has 1000 possible moves.
        self.observation_space = spaces.Box(0, 7, (128,), dtype=np.int32)

        self.board: np.ndarray = self.init_board()
        self.pieces: list[dict] = self.init_pieces()
        self.pieces_names: tuple = self.get_pieces_names()

        self.turn: int = Pieces.WHITE
        self.done: bool = False
        self.steps: int = 0
        self.checked: list[bool] = [False, False]
        self.max_steps: int = max_steps
        self.resources: list[int] = [0, 0]

        self.font: Font | None = None
        self.cell_size: int = window_size // 8
        self.screen: Surface | None = None
        self.window_size: int = window_size
        self.render_mode: str = render_mode

    @staticmethod
    def init_board() -> np.ndarray:
        board = np.zeros((2, 8, 8), dtype=np.uint8)
        board[:, 0, 3] = Pieces.QUEEN
        board[:, 0, 4] = Pieces.KING
        board[:, 1, :] = Pieces.PAWN
        board[:, 0, (0, 7)] = Pieces.ROOK
        board[:, 0, (1, 6)] = Pieces.KNIGHT
        board[:, 0, (2, 5)] = Pieces.BISHOP
        return board

    @staticmethod
    def init_pieces():
        pieces = {
            "pawn_1": (1, 0),
            "pawn_2": (1, 1),
            "pawn_3": (1, 2),
            "pawn_4": (1, 3),
            "pawn_5": (1, 4),
            "pawn_6": (1, 5),
            "pawn_7": (1, 6),
            "pawn_8": (1, 7),
            "rook_1": (0, 0),
            "rook_2": (0, 7),
            "knight_1": (0, 1),
            "knight_2": (0, 6),
            "bishop_1": (0, 2),
            "bishop_2": (0, 5),
            "queen": (0, 3),
            "king": (0, 4),
        }

        return [pieces.copy(), pieces.copy()]

    def get_state(self, turn: int) -> np.ndarray:
        arr = self.board.copy()
        if turn == Pieces.WHITE:
            arr[[0, 1]] = arr[[1, 0]]
        return arr.flatten()

    def draw_cells(self):
        for y in range(8):
            for x in range(8):
                self.draw_cell(x, y)

    def draw_pieces(self):
        for y in range(8):
            for x in range(8):
                self.draw_piece(x, y)

    def draw_axis(self):
        font = pygame.font.Font(None, 36)
        for i, label in enumerate("abcdefgh"):
            text = font.render(label, True, Colors.GREEN)
            self.screen.blit(text, (i * self.cell_size + self.cell_size // 2 - 10, self.window_size - 20))
        for i, label in enumerate("12345678"):
            text = font.render(label, True, Colors.GREEN)
            self.screen.blit(text, (self.window_size - 20, i * self.cell_size + self.cell_size // 2 - 10))

    def render(self) -> Union[None, np.ndarray]:
        self.init_pygame()
        self.screen.fill(Colors.BLACK)
        self.draw_cells()
        self.draw_pieces()
        self.draw_axis()

        if self.render_mode == "human":
            pygame.display.flip()
        else:
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )

    def init_pygame(self) -> None:
        if self.screen is not None:
            return
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font("chess/seguisym.ttf", self.cell_size // 2)
        if self.render_mode == "human":
            pygame.display.init()
            self.screen = pygame.display.set_mode((self.window_size,) * 2)
            pygame.display.set_caption("Chess RL Environment")
        else:
            self.screen = pygame.Surface((self.window_size,) * 2)

    @staticmethod
    def get_cell_color(x: int, y: int) -> tuple[int]:
        if (x + y) % 2 == 0:
            return Colors.GRAY
        return Colors.BLACK

    def get_left_top(self, x: int, y: int, offset: float = 0) -> tuple[float, float]:
        return self.cell_size * x + offset, self.cell_size * y + offset

    def draw_cell(self, x: int, y: int) -> None:
        pygame.draw.rect(
            self.screen,
            self.get_cell_color(x, y),
            pygame.Rect((*self.get_left_top(x, y), self.cell_size, self.cell_size)),
        )

    def draw_piece(self, x: int, y: int) -> None:
        row, col = y, x
        for color in [Pieces.BLACK, Pieces.WHITE]:

            if self.is_empty((row, col), color):
                continue

            yy = abs((color * 7) - y)
            text = self.font.render(
                Pieces.get_ascii(color, int(self.board[color, row, col])),
                True,
                Colors.WHITE,
                self.get_cell_color(x, yy),
            )
            rect = text.get_rect()
            rect.center = self.get_left_top(x, yy, offset=self.cell_size // 2)
            self.screen.blit(text, rect)

    def close(self) -> None:
        if self.screen is None:
            return
        pygame.display.quit()
        pygame.quit()

    def reset(self, **kwargs) -> None:
        self.done = False
        self.turn = Pieces.WHITE
        self.steps = 0
        self.board = self.init_board()
        self.pieces = self.init_pieces()
        self.pieces_names = self.get_pieces_names()
        self.checked = [False, False]
        self.resources = [0, 0]

    def get_pieces_names(self) -> tuple:
        zero = list(self.pieces[0].keys())
        one = list(self.pieces[1].keys())
        return zero, one

    def refresh_pieces_names(self):
        self.pieces_names = self.get_pieces_names()

    @staticmethod
    def is_in_range(pos: Cell) -> bool:
        row, col = pos
        return 0 <= row <= 7 and 0 <= col <= 7

    @staticmethod
    def get_size(name: str) -> int:
        return Moves.POSSIBLE_MOVES[name]

    def get_empty_actions(self, name: str) -> tuple[np.ndarray, np.ndarray]:
        size = self.get_size(name)
        possibles = np.zeros((size, 2), dtype=np.int32)
        actions_mask = np.zeros(size, dtype=np.int32)
        return possibles, actions_mask

    def is_path_empty(self, current_pos: Cell, next_pos: Cell, turn: int, except_pawn: bool = False) -> bool:
        next_row, next_col = next_pos
        current_row, current_col = current_pos

        diff_row = next_row - current_row
        diff_col = next_col - current_col
        sign_row = np.sign(next_row - current_row)
        sign_col = np.sign(next_col - current_col)

        size = max(abs(diff_row), abs(diff_col)) - 1
        rows = np.zeros(size, dtype=np.int32) + next_row
        cols = np.zeros(size, dtype=np.int32) + next_col

        if diff_row:
            rows = np.arange(current_row + sign_row, next_row, sign_row, dtype=np.int32)

        if diff_col:
            cols = np.arange(current_col + sign_col, next_col, sign_col, dtype=np.int32)

        for pos in zip(rows, cols):
            if except_pawn:
                if not self.both_side_empty_pawn(pos, turn):
                    return False
            else:
                if not self.both_side_empty(pos, turn):
                    return False

        return True

    def piece_can_jump(self, pos: Cell, turn: int) -> bool:
        jumps = {Pieces.KNIGHT, Pieces.KING, Pieces.WINGED_KNIGHT, Pieces.WARELEFANT}
        piece = self.board[turn, pos[0], pos[1]]
        return piece in jumps

    def is_path_empty_for_piece(self, current_pos: Cell, next_pos: Cell, turn: int) -> bool:
        this_piece = Pieces.EMPTY
        for dic in self.pieces:
            for key, val in dic.items():
                if val == current_pos:
                    this_piece = key.split("_")[0]

        if this_piece == "warelefant":
            return self.is_path_empty(current_pos, next_pos, turn, except_pawn=True)
        else:
            return (self.piece_can_jump(current_pos, turn)) or (self.is_path_empty(current_pos, next_pos, turn))

    def general_validation(self, current_pos: Cell, next_pos: Cell, turn: int, deny_enemy_king: bool) -> bool:
        if not self.is_in_range(next_pos):
            return False

        if not self.is_empty(next_pos, turn):
            return False

        if self.is_enemy_king(next_pos, turn) and (not deny_enemy_king):
            return False

        if not self.is_path_empty_for_piece(current_pos, next_pos, turn):
            return False
        return True

    def is_valid_move(
            self,
            current_pos: Cell,
            next_pos: Cell,
            turn: int,
            deny_enemy_king: bool,
    ) -> bool:
        if not self.general_validation(current_pos, next_pos, turn, deny_enemy_king):
            return False
        if self.is_lead_to_check(current_pos, next_pos, turn):
            return False
        return True

    def is_lead_to_check(self, current_pos: Cell, next_pos: Cell, turn: int) -> bool:
        temp = Chess(render_mode="rgb_array")
        temp.board = np.copy(self.board)
        temp.move_piece(current_pos, next_pos, turn)
        return temp.is_check(temp.get_pos_king(turn), turn)

    def get_piece(self, pos: Cell, turn: int) -> int:
        """
       Get the piece from the board at the given position and turn
       :param pos: position of the board where the piece is to be fetched from
       :param turn: turn of the player
       :return: Returns the index of the piece at the given location and turn
        """
        return int(self.board[turn, pos[0], pos[1]])

    def check_king_flank(self, king_position: Cell, direction: tuple[int, int], turn: int) -> bool:
        """
        Checks if the king's flank is under attack in a given direction.
        :param king_position: The position of the king on the chessboard.
        :param direction: The direction to check for the flank attack.
        :param turn: The current turn number.
        :return: True if the king's flank is under attack, False otherwise.
        """
        r, c = direction
        row, col = king_position
        while self.is_in_range((row, col)):
            if not self.is_empty((row, col), turn):
                piece = self.get_piece((row, col), turn)
                possibles, _ = self.get_empty_actions(Pieces.get_piece_name(piece))
                return king_position in possibles
            row += r
            col += c
        return False

    def check_king_flanks(self, king_position: Cell, turn: int) -> bool:
        """
        Check if the king is under attack from any of the 8 directions
        :param king_position: The position of the king on the chessboard.
        :param turn: The current turn number.
        :return: True if the king is under attack from any of the 8 directions, False otherwise
        """
        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            return self.check_king_flank(king_position, direction, turn)

    def check_all_pieces_check(self, king_position: Cell, turn: int) -> bool:
        """
        Check for all the pieces of the opponent if they can attack the king
        :param king_position: The position of the king on the chessboard.
        :param turn: The current turn number.
        :return: True if any of the pieces can attack the king, False otherwise.
        """
        for row in range(8):
            for col in range(8):
                if self.is_empty((row, col), 1 - turn):
                    continue
                piece = self.get_piece((row, col), 1 - turn)
                possibles, _, _ = self.get_all_actions(Pieces.get_piece_name(piece))
                if king_position in possibles:
                    return True
        return False

    def get_actions_for_piece(self, pos: Cell, turn: int, piece: str, moves: list[tuple[int, int]],
                              deny_enemy_king: bool = False):
        possibles, actions_mask = self.get_empty_actions(piece)
        if pos is None:
            return possibles, actions_mask

        row, col = pos
        for i, (r, c) in enumerate(moves):
            next_pos = (row + r, col + c)

            if not self.is_valid_move(pos, next_pos, turn, deny_enemy_king):
                continue

            possibles[i] = next_pos
            actions_mask[i] = 1

        return possibles, actions_mask

    def get_actions_for_rook(self, pos: Cell, turn: int, deny_enemy_king: bool = False):
        return self.get_actions_for_piece(pos, turn, "rook", Moves.ROOK, deny_enemy_king)

    def get_actions_for_bishop(self, pos: Cell, turn: int, deny_enemy_king: bool = False):
        return self.get_actions_for_piece(pos, turn, "bishop", Moves.BISHOP, deny_enemy_king)

    def get_actions_for_war_elefant(self, pos: Cell, turn: int, deny_enemy_king: bool = False):
        return self.get_actions_for_piece(pos, turn, "warelefant", Moves.WARELEFANT, deny_enemy_king)

    def get_action_for_queen(self, pos: Cell, turn: int, deny_enemy_king: bool = False):
        possibles_rook, actions_mask_rook = self.get_actions_for_rook(
            pos, turn, deny_enemy_king
        )
        possibles_bishop, actions_mask_bishop = self.get_actions_for_bishop(
            pos, turn, deny_enemy_king
        )
        possibles = np.concatenate([possibles_bishop, possibles_rook])
        actions_mask = np.concatenate([actions_mask_bishop, actions_mask_rook])

        return possibles, actions_mask

    def get_actions_for_dutchwaterline(self, turn: int) -> tuple:
        rows = [2, 3, 4, 5]
        all_possibles = []
        all_actions_mask = []
        all_source_pos = []
        count = 0

        for row in rows:
            for col in range(8):
                if not self.is_enemy_king((row, col), turn):
                    count += 1

                if (count == 8):
                    all_possibles.append([row, 0])
                    all_actions_mask.append(1)
                    all_source_pos.append([row, 0])

                if (col == 7):
                    count = 0

        return all_possibles, all_actions_mask, all_source_pos

    def get_actions_for_pawn(self, pos: Cell, turn: int, deny_enemy_king: bool = False):
        possibles, actions_mask = self.get_empty_actions("pawn")
        if pos is None:
            return possibles, actions_mask

        row, col = pos
        if self.board[turn, row, col] == Pieces.QUEEN:
            return self.get_action_for_queen(pos, turn)

        for i, (r, c) in enumerate(Moves.PAWN[:4]):
            next_pos = (row + r, col + c)

            if not self.is_valid_move(pos, next_pos, turn, deny_enemy_king):
                continue

            can_moves = (
                (r == 1 and c == 0 and self.both_side_empty(next_pos, turn)),
                (r == 2 and row == 1 and self.both_side_empty(next_pos, turn)),
                (r == 1 and abs(c) == 1 and self.check_for_enemy(next_pos, turn)),
                # TODO: EN PASSANT
            )

            if True in can_moves:
                possibles[i] = next_pos
                actions_mask[i] = 1

        return possibles, actions_mask

    def get_actions_for_knight(self, pos: Cell, turn: int, deny_enemy_king: bool = False):
        return self.get_actions_for_piece(pos, turn, "knight", Moves.KNIGHT, deny_enemy_king)

    def get_actions_for_hoplite(self, pos: Cell, turn: int, deny_enemy_king: bool = False):
        possibles, actions_mask = self.get_empty_actions("hoplite")
        if pos is None:
            return possibles, actions_mask

        row, col = pos
        if self.board[turn, row, col] == Pieces.QUEEN:
            return self.get_action_for_queen(pos, turn)

        for i, (r, c) in enumerate(Moves.HOPLITE[:4]):
            next_pos = (row + r, col + c)

            if not self.is_valid_move(pos, next_pos, turn, deny_enemy_king):
                continue

            can_moves = (
                (r == 1 and c == 0 and (self.both_side_empty(next_pos, turn) or self.check_for_enemy(next_pos, turn))),
                (r == 2 and row == 1 and self.both_side_empty(next_pos, turn)),
                (r == 1 and abs(c) == 1 and self.check_for_enemy(next_pos, turn)),
                # TODO: EN PASSANT
            )

            if True in can_moves:
                possibles[i] = next_pos
                actions_mask[i] = 1

        return possibles, actions_mask

    def get_actions_for_winged_knight(
            self, pos: Cell, turn: int, deny_enemy_king: bool = False
    ):
        possibles, actions_mask = self.get_empty_actions("wingedknight")

        if pos is None:
            return possibles, actions_mask

        row, col = pos
        for i, (r, c) in enumerate(Moves.WINGED_KNIGHT):
            next_pos = (row + r, col + c)
            if not self.is_valid_move(pos, next_pos, turn, deny_enemy_king):
                continue

            possibles[i] = next_pos
            actions_mask[i] = 1

        return possibles, actions_mask

    def get_actions_for_king(self, pos: Cell, turn: int):
        row, col = pos
        possibles, actions_mask = self.get_empty_actions("king")

        for i, (r, c) in enumerate(Moves.KING):
            next_pos = (row + r, col + c)

            if not self.is_valid_move(pos, next_pos, turn, False):
                continue

            if self.is_neighbor_enemy_king(next_pos, turn):
                continue

            possibles[i] = next_pos
            actions_mask[i] = 1
        return possibles, actions_mask

    def get_source_pos(self, name: str, turn: int):
        cat = name.split("_")[0]
        pos = self.pieces[turn][name]
        if pos is None:
            pos = (0, 0)
        size = self.get_size(cat)
        return np.array([pos] * size)

    def get_actions_for(self, name: str, turn: int, deny_enemy_king: bool = False) -> tuple:
        assert name in self.pieces_names[turn], f"{name} not in {self.pieces_names[turn]}"
        piece_cat = name.split("_")[0]
        piece_pos = self.pieces[turn][name]
        src_poses = self.get_source_pos(name, turn)

        if piece_cat == "pawn":
            return (
                src_poses,
                *self.get_actions_for_pawn(piece_pos, turn, deny_enemy_king),
            )

        if piece_cat == "hoplite":
            return (
                src_poses,
                *self.get_actions_for_hoplite(piece_pos, turn, deny_enemy_king),
            )

        if piece_cat == "knight":
            return (
                src_poses,
                *self.get_actions_for_knight(piece_pos, turn, deny_enemy_king),
            )

        if piece_cat == "wingedknight":
            return (
                src_poses,
                *self.get_actions_for_winged_knight(piece_pos, turn, deny_enemy_king),
            )

        if piece_cat == "rook":
            return (
                src_poses,
                *self.get_actions_for_rook(piece_pos, turn, deny_enemy_king),
            )

        if piece_cat == "warelefant":
            return (
                src_poses,
                *self.get_actions_for_war_elefant(piece_pos, turn, deny_enemy_king),
            )

        if piece_cat == "bishop":
            return (
                src_poses,
                *self.get_actions_for_bishop(piece_pos, turn, deny_enemy_king),
            )

        if piece_cat == "queen":
            return (
                src_poses,
                *self.get_action_for_queen(piece_pos, turn, deny_enemy_king),
            )

        if piece_cat == "king":
            return (
                src_poses,
                *self.get_actions_for_king(piece_pos, turn),
            )

    def get_all_actions(self, turn: int, deny_enemy_king: bool = False):
        all_possibles = []
        all_source_pos = []
        all_actions_mask = []
        length = 0
        for name in self.pieces[turn].keys():
            # DENY ENEMY KING == FOR CHECKMATE VALIDATION ONLY SO ....
            if name == "king" and deny_enemy_king:
                continue

            source_pos, possibles, actions_mask = self.get_actions_for(
                name, turn, deny_enemy_king
            )

            all_source_pos.append(source_pos)
            all_possibles.append(possibles)
            all_actions_mask.append(actions_mask)
            length += len(actions_mask)

        for i in range(3):
            source_pos, possibles, actions_mask = self.get_card_upgrade_actions(turn, i)

            all_source_pos.append(source_pos)
            all_possibles.append(possibles)
            all_actions_mask.append(actions_mask)
            length += len(actions_mask)

        if (self.resources[turn] > 4):
            possibles, actions_mask, source_pos = self.get_actions_for_dutchwaterline(
                turn
            )

            all_possibles.append(possibles)
            all_actions_mask.append(actions_mask)
            all_source_pos.append(source_pos)
            length += len(actions_mask)

        all_actions_mask.append(np.zeros(self.action_space_length - length, dtype=bool))
        return (
            np.concatenate(all_source_pos),
            np.concatenate(all_possibles),
            np.concatenate(all_actions_mask),
        )

    def get_card_upgrade_actions(self, turn: int, card_id: int):
        match card_id:
            case 0:
                return self.get_pawn_upgrade_actions(turn)
            case 1:
                return self.get_knight_upgrade_actions(turn)
            case 2:
                return self.get_rook_upgrade_actions(turn)
            case _:
                assert False, f"Invalid card id {card_id}"

    def get_pawn_upgrade_actions(self, turn: int):
        source_pos, possibles, actions_mask, pieces = self.get_empty_upgrade_actions(turn, Pieces.PAWN)
        if self.resources[turn] >= 2:
            for i, piece in enumerate(pieces):
                if self.pieces[turn][piece] is None:
                    continue

                possibles[i] = self.pieces[turn][piece]
                actions_mask[i] = 1

        return source_pos, possibles, actions_mask

    def get_knight_upgrade_actions(self, turn: int):
        source_pos, possibles, actions_mask, pieces = self.get_empty_upgrade_actions(turn, Pieces.KNIGHT)
        if self.resources[turn] >= 3:
            for i, piece in enumerate(pieces):
                if self.pieces[turn][piece] is None:
                    continue

                possibles[i] = self.pieces[turn][piece]
                actions_mask[i] = 1

        return source_pos, possibles, actions_mask

    def get_rook_upgrade_actions(self, turn: int):
        source_pos, possibles, actions_mask, pieces = self.get_empty_upgrade_actions(turn, Pieces.ROOK)
        if self.resources[turn] >= 5:
            for i, piece in enumerate(pieces):
                if self.pieces[turn][piece] is None:
                    continue

                possibles[i] = self.pieces[turn][piece]
                actions_mask[i] = 1

        return source_pos, possibles, actions_mask

    def get_empty_upgrade_actions(self, turn: int, piece: Pieces):
        # get all pieces with the same type
        pieces = [key for key in self.pieces[turn].keys() if key.split("_")[0] == Pieces.get_piece_name(piece).lower()]
        possibles = np.zeros((len(pieces), 2), dtype=np.int32)
        actions_mask = np.zeros(len(pieces), dtype=np.int32)
        source_pos = np.zeros((len(pieces), 2), dtype=np.int32)
        for i, piece in enumerate(pieces):
            if self.pieces[turn][piece] is None:
                continue

            possibles[i] = [0, 0]
            source_pos[i] = self.pieces[turn][piece]
        return source_pos, possibles, actions_mask, pieces

    def check_for_enemy(self, pos: Cell, turn: int) -> bool:
        r, c = pos
        return not self.is_empty((7 - r, c), 1 - turn)

    def is_empty(self, pos: Cell, turn: int) -> bool:
        return self.board[turn, pos[0], pos[1]] == Pieces.EMPTY

    def is_empty_pawn(self, pos: Cell, turn: int) -> bool:
        return self.board[turn, pos[0], pos[1]] == Pieces.EMPTY or self.board[turn, pos[0], pos[1]] == Pieces.PAWN or \
            self.board[turn, pos[0], pos[1]] == Pieces.HOPLITE

    def is_enemy_king(self, pos: Cell, turn: int) -> bool:
        r, c = pos
        return self.board[1 - turn, 7 - r, c] == Pieces.KING

    def both_side_empty(self, pos: Cell, turn: int) -> bool:
        r, c = pos
        return self.is_empty(pos, turn) and self.is_empty((7 - r, c), 1 - turn)

    def both_side_empty_pawn(self, pos: Cell, turn: int) -> bool:
        r, c = pos
        return self.is_empty_pawn(pos, turn) and self.is_empty_pawn((7 - r, c), 1 - turn)

    def get_pos_king(self, turn: int) -> Cell:
        row, col = np.nonzero(self.board[turn] == Pieces.KING)
        return row[0], col[0]

    def is_neighbor_enemy_king(self, pos: Cell, turn: int) -> bool:
        row, col = pos
        row_enemy_king, col_enemy_king = self.get_pos_king(1 - turn)
        row_enemy_king = 7 - row_enemy_king
        diff_row = abs(row - row_enemy_king)
        diff_col = abs(col - col_enemy_king)
        return diff_row <= 1 and diff_col <= 1

    def is_check(self, king_pos: Cell, turn: int) -> bool:
        rk, ck = king_pos

        diagonal_pieces = [Pieces.BISHOP, Pieces.QUEEN]
        straight_pieces = [Pieces.ROOK, Pieces.QUEEN, Pieces.WARELEFANT]

        # GO TO UP ROW
        for r in range(rk + 1, 8):
            if not self.is_empty((r, ck), turn):
                break
            p = self.board[1 - turn, 7 - r, ck]
            if p in straight_pieces:
                return True

        # GO TO DOWN ROW
        for r in range(rk - 1, -1, -1):
            if not self.is_empty((r, ck), turn):
                break
            p = self.board[1 - turn, 7 - r, ck]
            if p in straight_pieces:
                return True

        # GO TO RIGHT COL
        for c in range(ck + 1, 8):
            if not self.is_empty((rk, c), turn):
                break
            p = self.board[1 - turn, 7 - rk, c]
            if p in straight_pieces:
                return True

        # GOT TO LEFT COL
        for c in range(ck - 1, -1, -1):
            if not self.is_empty((rk, c), turn):
                break
            p = self.board[1 - turn, 7 - rk, c]
            if p in straight_pieces:
                return True

        # CROSS DOWN
        for r in range(rk + 1, 8):
            # RIGHT
            d = r - rk
            for c in [ck + d, ck - d]:
                if not self.is_in_range((r, c)):
                    continue

                if not self.is_empty((r, c), turn):
                    break

                p = self.board[1 - turn, 7 - r, c]

                if p in diagonal_pieces:
                    return True

                if d == 1 and (p == Pieces.PAWN or p == Pieces.HOPLITE):
                    return True

        # CROSS UP
        for r in range(rk - 1, -1, -1):
            d = r - rk
            for c in [ck + d, ck - d]:
                if not self.is_in_range((r, c)):
                    continue

                if not self.is_empty((r, c), turn):
                    break

                p = self.board[1 - turn, 7 - r, c]
                if p in diagonal_pieces:
                    return True

                if d == 1 and (p == Pieces.PAWN or p == Pieces.HOPLITE):
                    return True

        # KNIGHTS
        for r, c in Moves.KNIGHT:
            nr, nc = rk + r, ck + c
            if not self.is_in_range((nr, nc)):
                continue
            if self.board[1 - turn, 7 - nr, nc] == Pieces.KNIGHT:
                return True

        # WINGED KNIGHTS
        for r, c in Moves.WINGED_KNIGHT:
            nr, nc = rk + r, ck + c
            if not self.is_in_range((nr, nc)):
                continue
            if self.board[1 - turn, 7 - nr, nc] == Pieces.WINGED_KNIGHT:
                return True
        return False

    def update_checks(self, rewards: list[int] = None, infos: list[set] = None):
        rewards = [0, 0] if rewards is None else rewards
        infos = [set(), set()] if infos is None else infos

        for turn in range(2):
            king_pos = self.get_pos_king(turn)
            is_check = self.is_check(king_pos, turn)
            self.checked[turn] = is_check
            if is_check:
                rewards[turn] += Rewards.CHECK_LOSE
                rewards[1 - turn] += Rewards.CHECK_WIN

                infos[turn].add(InfoKeys.CHECK_LOSE)
                infos[1 - turn].add(InfoKeys.CHECK_WIN)
                break
        return rewards, infos

    def update_check_mates(self, rewards: list[int] = None, infos: list[set] = None):
        rewards = [0, 0] if rewards is None else rewards
        infos = [set(), set()] if infos is None else infos

        for turn in range(2):
            _, _, actions = self.get_all_actions(turn)
            if np.sum(actions) == 0:
                self.done = True
                rewards[turn] += Rewards.CHECK_MATE_LOSE
                rewards[1 - turn] += Rewards.CHECK_MATE_WIN

                infos[turn].add(InfoKeys.CHECK_MATE_LOSE)
                infos[1 - turn].add(InfoKeys.CHECK_MATE_WIN)
                break

        return rewards, infos

    def update_draw(self, rewards: list[int] = None, infos: list[set] = None):
        rewards = [0, 0] if rewards is None else rewards
        infos = [set(), set()] if infos is None else infos

        if self.steps >= self.max_steps:
            rewards[0] += Rewards.DRAW
            rewards[1] += Rewards.DRAW

            infos[0].add(InfoKeys.DRAW)
            infos[1].add(InfoKeys.DRAW)

        return rewards, infos

    def dutchwaterline(self, row: Cell):
        row = row[0]
        row_turn1 = 7 - row
        for turn in range(2):
            for col in range(8):
                # Check if the piece is a king before removing it
                if self.board[turn, row if turn == 0 else row_turn1, col] != Pieces.KING:
                    self.board[turn, row if turn == 0 else row_turn1, col] = Pieces.EMPTY

    def move_piece(self, current_pos: Cell, next_pos: Cell, turn: int):
        next_row, next_col = next_pos
        current_row, current_col = current_pos
        self.board[turn, next_row, next_col] = self.board[
            turn, current_row, current_col
        ]
        # Set default rewards, [-1, -2], -1 for the player who moved the piece, -2 for the other player
        rewards = [Rewards.MOVE, Rewards.MOVE]
        rewards[1 - turn] *= 0

        self.capture_pawn_by_warelefant(next_row, next_col, current_row, current_col, turn)
        self.promote_pawn_or_hoplite(next_pos, turn)
        self.board[turn, current_row, current_col] = Pieces.EMPTY
        self.board[1 - turn, 7 - next_row, next_col] = Pieces.EMPTY

        for (key, value) in self.pieces[turn].items():
            if value == tuple(current_pos):
                # # Update the location of the piece in the pieces array
                self.pieces[turn][key] = tuple(next_pos)

        for (key, value) in self.pieces[1 - turn].items():
            if value == (7 - next_pos[0], next_pos[1]):
                # Remove the location from the piece that was removed in the pieces array
                self.pieces[1 - turn][key] = None

                # add a reward for capturing a piece
                piece = key.split("_")[0]
                piece = piece.upper()

                # get the reward from the rewards.py based on the name of the piece
                reward = getattr(Rewards, piece)
                rewards = self.add_reward(rewards, reward, turn)

        return rewards, [set(), set()]

    @staticmethod
    def add_reward(rewards: list[int] = None, reward: int = 0, turn: int = 1):
        rewards = [Rewards.MOVE, Rewards.MOVE] if rewards is None else rewards
        rewards[turn] += reward
        rewards[1 - turn] += -reward
        return rewards

    def capture_pawn_by_warelefant(self, next_row: int, next_col: int, current_row: int, current_col: int, turn: int):
        if self.board[turn, next_row, next_col] == Pieces.WARELEFANT:
            if current_row == next_row:
                start_col = min(current_col, next_col) + 1
                end_col = max(current_col, next_col)
                for col in range(start_col, end_col):
                    if self.board[turn, current_row, col] in [Pieces.PAWN, Pieces.HOPLITE]:
                        self.board[turn, current_row, col] = Pieces.EMPTY
                        self.board[1 - turn, 7 - current_row, col] = Pieces.EMPTY
                        for key, value in self.pieces[turn].items():
                            if value == (current_row, col):
                                self.pieces[turn][key] = None
                        for key, value in self.pieces[1 - turn].items():
                            if value == (7 - current_row, col):
                                self.pieces[1 - turn][key] = None

            elif current_col == next_col:
                start_row = min(current_row, next_row) + 1
                end_row = max(current_row, next_row)
                for row in range(start_row, end_row):
                    if (self.board[turn, row, current_col] in [Pieces.PAWN, Pieces.HOPLITE] or
                            self.board[1 - turn, 7 - row, current_col] in [Pieces.PAWN, Pieces.HOPLITE]):
                        self.board[turn, row, current_col] = Pieces.EMPTY
                        self.board[1 - turn, 7 - row, current_col] = Pieces.EMPTY
                        for key, value in self.pieces[turn].items():
                            if value == (row, current_col):
                                self.pieces[turn][key] = None
                        for key, value in self.pieces[1 - turn].items():
                            if value == (7 - row, current_col):
                                self.pieces[1 - turn][key] = None

    def is_game_done(self):
        return self.done or (self.steps >= self.max_steps)

    def promote_pawn_or_hoplite(self, pos: Cell, turn: int):
        row, col = pos
        if (self.board[turn, row, col] == Pieces.PAWN or self.board[turn, row, col] == Pieces.HOPLITE) and row == 7:
            self.board[turn, row, col] = Pieces.QUEEN

    def upgrade_piece(self, pos: Cell, turn: int, piece_to_upgrade: Pieces):
        self.refresh_pieces_names()
        row, col = pos
        rewards = [0, 0]
        rewards[turn] = Rewards.UPGRADE_PIECE
        rewards[1 - turn] = 0
        new_piece = Pieces.get_upgraded_variant(piece_to_upgrade)

        # get piece_name from position
        piece_name = None
        for key, value in self.pieces[turn].items():
            if value == (row, col):
                piece_name = key
                break

        # return rewards if the piece is empty (This happens because of dutch waterline,
        # which can be activated on an empty space)
        if new_piece == Pieces.EMPTY or piece_name is None:
            return [0, 0], [set(), set()]

        split_piece_name = piece_name.split("_")

        if len(split_piece_name) < 2:
            print(piece_name)
            return [0, 0], [set(), set()]

        # update the piece
        self.pieces[turn][f"{Pieces.get_piece_name(new_piece).lower()}_{piece_name.split('_')[1]}"] = self.pieces[
            turn].pop(piece_name)
        self.refresh_pieces_names()
        self.board[turn, row, col] = new_piece
        self.remove_resources(turn, new_piece)
        return rewards, [set(), set()]

    def remove_resources(self, turn: int, piece: Pieces):
        match piece:
            case Pieces.HOPLITE:
                self.resources[turn] -= 2
            case Pieces.WINGED_KNIGHT:
                self.resources[turn] -= 3
            case Pieces.WARELEFANT:
                self.resources[turn] -= 5

    def step(self, action: int) -> tuple[list[int], bool, list[set]]:
        assert not self.is_game_done(), "the game is finished reset"
        assert action < self.action_space_length, f"action number must be less than {self.action_space_length}."

        source_pos, possibles, actions_mask = self.get_all_actions(self.turn)
        assert actions_mask[action], f"Cannot Take This Action = {action}, {source_pos[action]} -> {possibles[action]}"

        from_pos = Cell((source_pos[action][0], source_pos[action][1]))
        next_pos = Cell((possibles[action][0], possibles[action][1]))

        if from_pos == next_pos:
            source_pos_piece = self.board[self.turn, from_pos[0], from_pos[1]]
            rewards, infos = self.upgrade_piece(from_pos, self.turn, source_pos_piece)
            end_turn = False
        else:
            rewards, infos = self.move_piece(
                from_pos, next_pos, self.turn
            )
            end_turn = True

        if (from_pos == (2, 0) or from_pos == (3, 0) or from_pos == (4, 0) or from_pos == (5, 0)
                and from_pos == next_pos):
            self.dutchwaterline(from_pos)
            rewards = self.add_reward(None, Rewards.DUTCH_WATERLINE, self.turn)
            end_turn = False

        rewards, infos = self.update_checks(rewards, infos)
        rewards, infos = self.update_check_mates(rewards, infos)
        rewards, infos = self.update_draw(rewards, infos)

        if from_pos != next_pos or end_turn:
            self.resources[self.turn] += 1
            self.turn = 1 - self.turn
        self.steps += 1
        return rewards, self.is_game_done(), infos

    def can_castle(self, turn):
        # Check if the king is in check
        if self.is_check(self.get_pos_king(turn), turn):
            return False

        # Check if the king and rooks have not moved
        if self.has_moved('king', turn) or self.has_moved('rook_1', turn) or self.has_moved('rook_2', turn):
            return False

        # Check if the path between the king and the rooks is empty
        king_pos = self.get_pos_king(turn)
        rook_1_pos = self.pieces[turn]['rook_1']
        rook_2_pos = self.pieces[turn]['rook_2']

        # check values for None type
        if king_pos is None or rook_1_pos is None or rook_2_pos is None:
            return False

        if not self.is_path_empty(king_pos, rook_1_pos, turn) or not self.is_path_empty(king_pos, rook_2_pos, turn):
            return False

        # If all conditions are met, return True
        return True

    def has_moved(self, param: str, turn: int) -> bool:
        # Get the current position of the piece
        current_pos = self.pieces[turn][param]

        # Get the initial position of the piece
        initial_pos = self.init_pieces()[turn][param]

        # Check if the current position is different from the initial position
        return current_pos != initial_pos

    def set_board(self, board: np.array) -> None:
        self.board = board
        self.pieces = self.get_pieces_from_board(board)
        self.pieces_names = self.get_pieces_names()

    def get_pieces_from_board(self, board: np.array) -> list[dict]:
        pieces_0 = self.get_pieces_from_board_side(board[0])
        pieces_1 = self.get_pieces_from_board_side(board[1])
        return [pieces_0, pieces_1]

    @staticmethod
    def get_pieces_from_board_side(board_side: np.array) -> dict:
        pieces = {}
        counter = 1
        for i, row in enumerate(board_side):
            for j, piece in enumerate(row):
                if piece != 0:
                    name = Pieces.get_piece_name(piece)

                    pieces[name + "_" + str(counter)] = (i, j)
                    counter += 1
        return pieces
