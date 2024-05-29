import gym
import numpy as np
from gym import spaces

import chess.constants.info_keys as InfoKeys
import chess.constants.moves as Moves
import chess.constants.rewards as Rewards
import chess.pieces as Pieces
from chess.models.board import AoWBoard
from chess.models.types import Cell
from chess.utils.pygame import PyGameUtils


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

        self.turn: int = Pieces.WHITE
        self.done: bool = False
        self.steps: int = 0
        self.checked: list[bool] = [False, False]
        self.max_steps: int = max_steps

        self.pygame_utils = PyGameUtils(render_mode=render_mode, window_size=window_size)
        self.aow_board = AoWBoard()

    def reset(self, **kwargs) -> None:
        self.done = False
        self.turn = Pieces.WHITE
        self.steps = 0
        self.checked = [False, False]
        self.aow_board.reset()

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
        piece = self.aow_board.get_piece(pos, turn)
        return piece in jumps

    def is_path_empty_for_piece(self, current_pos: Cell, next_pos: Cell, turn: int) -> bool:
        this_piece = Pieces.EMPTY
        for dic in self.aow_board.pieces:
            for key, val in dic.items():
                if val == current_pos:
                    this_piece = key.split("_")[0]

        if this_piece == "warelefant":
            return self.is_path_empty(current_pos, next_pos, turn, except_pawn=True)
        else:
            return (self.piece_can_jump(current_pos, turn)) or (self.is_path_empty(current_pos, next_pos, turn))

    def general_validation(self, current_pos: Cell, next_pos: Cell, turn: int, deny_enemy_king: bool) -> bool:
        if not self.aow_board.is_in_range(next_pos):
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
        temp.aow_board.board = self.aow_board.copy_board()
        temp.move_piece(current_pos, next_pos, turn)
        # return temp.check_all_pieces_check(temp.aow_board.get_pos_king(turn), turn)
        return temp.is_check(temp.aow_board.get_pos_king(turn), turn)

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
        while self.aow_board.is_in_range(Cell(row, col)):
            if not self.is_empty(Cell(row, col), turn):
                piece = self.aow_board.get_piece(Cell(row, col), turn)
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
                if self.is_empty(Cell(row, col), 1 - turn):
                    continue
                piece = self.aow_board.get_piece(Cell(row, col), 1 - turn)
                possibles, _ = self.get_all_actions_for_piece(Cell(row, col), 1 - turn, piece)
                if king_position in possibles:
                    return True
        return False

    def get_all_actions_for_piece(self, cell: Cell, turn: int, piece: int) -> tuple:
        """
        Get all possible actions for a given piece at a given cell
        :param cell: The cell where the piece is located
        :param turn: The current turn number
        :param piece: The piece to get the actions for
        :return: A tuple containing the source positions, possible actions and the action mask
        """

        match piece:
            case Pieces.PAWN:
                return self.get_actions_for_pawn(cell, turn)
            case Pieces.HOPLITE:
                return self.get_actions_for_hoplite(cell, turn)
            case Pieces.KNIGHT:
                return self.get_actions_for_knight(cell, turn)
            case Pieces.WINGED_KNIGHT:
                return self.get_actions_for_winged_knight(cell, turn)
            case Pieces.ROOK:
                return self.get_actions_for_rook(cell, turn)
            case Pieces.WARELEFANT:
                return self.get_actions_for_war_elefant(cell, turn)
            case Pieces.BISHOP:
                return self.get_actions_for_bishop(cell, turn)
            case Pieces.QUEEN:
                return self.get_action_for_queen(cell, turn)
            case Pieces.KING:
                return self.get_actions_for_king(cell, turn)
            case _:
                return self.get_empty_actions(Pieces.get_piece_name(piece))

    def get_actions_for_piece(self, pos: Cell, turn: int, piece: str, moves: list[tuple[int, int]],
                              deny_enemy_king: bool = False):
        possibles, actions_mask = self.get_empty_actions(piece)
        if pos is None:
            return possibles, actions_mask

        row, col = pos
        for i, (r, c) in enumerate(moves):
            next_pos = Cell(row + r, col + c)

            if not self.is_valid_move(Cell(row, col), next_pos, turn, deny_enemy_king):
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
                if not self.is_enemy_king(Cell(row, col), turn):
                    count += 1

                if count == 8:
                    all_possibles.append([row, 0])
                    all_actions_mask.append(1)
                    all_source_pos.append([row, 0])

                if col == 7:
                    count = 0

        return all_possibles, all_actions_mask, all_source_pos

    def get_actions_for_pawn(self, pos: Cell | None, turn: int, deny_enemy_king: bool = False):
        possibles, actions_mask = self.get_empty_actions("pawn")
        if pos is None:
            return possibles, actions_mask

        row, col = pos
        if self.aow_board.is_piece(turn, Cell(row, col), Pieces.QUEEN):
            return self.get_action_for_queen(Cell(row, col), turn)

        for i, (r, c) in enumerate(Moves.PAWN[:4]):
            next_pos = Cell(row + r, col + c)

            if not self.is_valid_move(Cell(row, col), next_pos, turn, deny_enemy_king):
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

    def get_actions_for_knight(self, pos: Cell | None, turn: int, deny_enemy_king: bool = False):
        return self.get_actions_for_piece(pos, turn, "knight", Moves.KNIGHT, deny_enemy_king)

    def get_actions_for_hoplite(self, pos: Cell | None, turn: int, deny_enemy_king: bool = False):
        possibles, actions_mask = self.get_empty_actions("hoplite")
        if pos is None:
            return possibles, actions_mask

        row, col = pos
        if self.aow_board.is_piece(turn, Cell(row, col), Pieces.QUEEN):
            return self.get_action_for_queen(Cell(row, col), turn)

        for i, (r, c) in enumerate(Moves.HOPLITE[:4]):
            next_pos = Cell(row + r, col + c)

            if not self.is_valid_move(Cell(row, col), next_pos, turn, deny_enemy_king):
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
            self, pos: Cell | None, turn: int, deny_enemy_king: bool = False
    ):
        possibles, actions_mask = self.get_empty_actions("wingedknight")

        if pos is None:
            return possibles, actions_mask

        row, col = pos
        for i, (r, c) in enumerate(Moves.WINGED_KNIGHT):
            next_pos = Cell(row + r, col + c)
            if not self.is_valid_move(Cell(row, col), next_pos, turn, deny_enemy_king):
                continue

            possibles[i] = next_pos
            actions_mask[i] = 1

        return possibles, actions_mask

    def get_actions_for_king(self, pos: Cell, turn: int):
        row, col = pos
        possibles, actions_mask = self.get_empty_actions("king")

        for i, (r, c) in enumerate(Moves.KING):
            next_pos = Cell(row + r, col + c)

            if not self.is_valid_move(Cell(row, col), next_pos, turn, False):
                continue

            if self.is_neighbor_enemy_king(next_pos, turn):
                continue

            possibles[i] = next_pos
            actions_mask[i] = 1
        return possibles, actions_mask

    def get_source_pos(self, name: str, turn: int):
        cat = name.split("_")[0]
        pos = self.aow_board.pieces[turn][name]
        if pos is None:
            pos = (0, 0)
        size = self.get_possibles_size(cat)
        return np.array([pos] * size)

    def get_actions_for(self, name: str, turn: int, deny_enemy_king: bool = False) -> tuple:
        assert name in self.aow_board.get_pieces_names()[
            turn], f"{name} not in {self.aow_board.get_pieces_names()[turn]}"
        piece_cat = name.split("_")[0]
        piece_pos = self.aow_board.pieces[turn][name]
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
        for name in self.aow_board.pieces[turn].keys():
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

        if self.aow_board.get_resources(turn) > 4:
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
        if self.aow_board.get_resources(turn) >= 2:
            for i, piece in enumerate(pieces):
                if self.aow_board.pieces[turn][piece] is None:
                    continue

                possibles[i] = self.aow_board.pieces[turn][piece]
                actions_mask[i] = 1

        return source_pos, possibles, actions_mask

    def get_knight_upgrade_actions(self, turn: int):
        source_pos, possibles, actions_mask, pieces = self.get_empty_upgrade_actions(turn, Pieces.KNIGHT)
        if self.aow_board.get_resources(turn) >= 3:
            for i, piece in enumerate(pieces):
                if self.aow_board.pieces[turn][piece] is None:
                    continue

                possibles[i] = self.aow_board.pieces[turn][piece]
                actions_mask[i] = 1

        return source_pos, possibles, actions_mask

    def get_rook_upgrade_actions(self, turn: int):
        source_pos, possibles, actions_mask, pieces = self.get_empty_upgrade_actions(turn, Pieces.ROOK)
        if self.aow_board.get_resources(turn) >= 5:
            for i, piece in enumerate(pieces):
                if self.aow_board.pieces[turn][piece] is None:
                    continue

                possibles[i] = self.aow_board.pieces[turn][piece]
                actions_mask[i] = 1

        return source_pos, possibles, actions_mask

    def get_empty_upgrade_actions(self, turn: int, piece: Pieces):
        # get all pieces with the same type
        pieces = [key for key in self.aow_board.pieces[turn].keys() if
                  key.split("_")[0] == Pieces.get_piece_name(piece).lower()]
        possibles = np.zeros((len(pieces), 2), dtype=np.int32)
        actions_mask = np.zeros(len(pieces), dtype=np.int32)
        source_pos = np.zeros((len(pieces), 2), dtype=np.int32)
        for i, piece in enumerate(pieces):
            if self.aow_board.pieces[turn][piece] is None:
                continue

            possibles[i] = [0, 0]
            source_pos[i] = self.aow_board.pieces[turn][piece]
        return source_pos, possibles, actions_mask, pieces

    def check_for_enemy(self, pos: Cell, turn: int) -> bool:
        r, c = pos
        return not self.is_empty(Cell(7 - r, c), 1 - turn)

    def is_empty(self, pos: Cell, turn: int) -> bool:
        return not self.aow_board.is_piece(turn, pos)

    def is_empty_pawn(self, pos: Cell, turn: int) -> bool:
        return self.is_empty(pos, turn) or self.aow_board.is_piece(turn, pos, Pieces.PAWN) or \
            self.aow_board.is_piece(turn, pos, Pieces.HOPLITE)

    def is_enemy_king(self, pos: Cell, turn: int) -> bool:
        r, c = pos
        return self.aow_board.is_piece(1 - turn, Cell(7 - r, c), Pieces.KING)

    def both_side_empty(self, pos: Cell, turn: int) -> bool:
        r, c = pos
        return self.is_empty(Cell(r, c), turn) and self.is_empty(Cell(7 - r, c), 1 - turn)

    def both_side_empty_pawn(self, pos: Cell, turn: int) -> bool:
        r, c = pos
        return self.is_empty_pawn(pos, turn) and self.is_empty_pawn(Cell(7 - r, c), 1 - turn)

    def is_neighbor_enemy_king(self, pos: Cell, turn: int) -> bool:
        row, col = pos
        row_enemy_king, col_enemy_king = self.aow_board.get_pos_king(1 - turn)
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
            if not self.is_empty(Cell(r, ck), turn):
                break
            p = self.aow_board.get_piece(Cell(7 - r, ck), 1 - turn)
            if p in straight_pieces:
                return True

        # GO TO DOWN ROW
        for r in range(rk - 1, -1, -1):
            if not self.is_empty(Cell(r, ck), turn):
                break
            p = self.aow_board.get_piece(Cell(7 - r, ck), 1 - turn)
            if p in straight_pieces:
                return True

        # GO TO RIGHT COL
        for c in range(ck + 1, 8):
            if not self.is_empty(Cell(rk, c), turn):
                break
            p = self.aow_board.get_piece(Cell(7 - rk, c), 1 - turn)
            if p in straight_pieces:
                return True

        # GOT TO LEFT COL
        for c in range(ck - 1, -1, -1):
            if not self.is_empty(Cell(rk, c), turn):
                break
            p = self.aow_board.get_piece(Cell(7 - rk, c), 1 - turn)
            if p in straight_pieces:
                return True

        # CROSS DOWN
        for r in range(rk + 1, 8):
            # RIGHT
            d = r - rk
            for c in [ck + d, ck - d]:
                if not self.aow_board.is_in_range(Cell(r, c)):
                    continue

                if not self.is_empty(Cell(r, c), turn):
                    break

                p = self.aow_board.get_piece(Cell(7 - r, c), 1 - turn)

                if p in diagonal_pieces:
                    return True

                if d == 1 and (p == Pieces.PAWN or p == Pieces.HOPLITE):
                    return True

        # CROSS UP
        for r in range(rk - 1, -1, -1):
            d = r - rk
            for c in [ck + d, ck - d]:
                if not self.aow_board.is_in_range(Cell(r, c)):
                    continue

                if not self.is_empty(Cell(r, c), turn):
                    break

                p = self.aow_board.get_piece(Cell(7 - r, c), 1 - turn)
                if p in diagonal_pieces:
                    return True

                if d == 1 and (p == Pieces.PAWN or p == Pieces.HOPLITE):
                    return True

        # KNIGHTS
        for r, c in Moves.KNIGHT:
            nr, nc = rk + r, ck + c
            if not self.aow_board.is_in_range(Cell(nr, nc)):
                continue
            if self.aow_board.is_piece(1 - turn, Cell(7 - nr, nc), Pieces.KNIGHT):
                return True

        # WINGED KNIGHTS
        for r, c in Moves.WINGED_KNIGHT:
            nr, nc = rk + r, ck + c
            if not self.aow_board.is_in_range(Cell(nr, nc)):
                continue
            if self.aow_board.is_piece(1 - turn, Cell(7 - nr, nc), Pieces.WINGED_KNIGHT):
                return True
        return False

    def update_checks(self, rewards: list[int] = None, infos: list[set] = None):
        rewards = [0, 0] if rewards is None else rewards
        infos = [set(), set()] if infos is None else infos

        for turn in range(2):
            king_pos = self.aow_board.get_pos_king(turn)
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

    def dutchwaterline(self, pos: Cell):
        row = pos.row
        row_turn1 = 7 - row
        for turn in range(2):
            for col in range(8):
                # Check if the piece is a king before removing it
                row = row if turn == 0 else row_turn1
                if not self.aow_board.is_piece(turn, Cell(row, col), Pieces.KING):
                    self.aow_board.set_piece(turn, Cell(row, col), Pieces.EMPTY)

    def move_piece(self, src: Cell, dst: Cell, turn: int):
        piece = self.aow_board.get_piece(src, turn)

        # move piece
        self.aow_board.set_piece(turn, src, Pieces.EMPTY)
        self.aow_board.set_piece(turn, dst, piece)

        # remove enemy piece in position
        self.aow_board.set_piece(1 - turn, Cell(7 - dst.row, dst.col), Pieces.EMPTY)

        # Set default rewards, [-1, -2], -1 for the player who moved the piece, -2 for the other player
        rewards = [Rewards.MOVE, Rewards.MOVE]
        rewards[1 - turn] *= 0

        self.capture_pawn_by_warelefant(dst.row, dst.col, src.row, src.col, turn)
        self.promote_pawn_or_hoplite(dst, turn)

        for (key, value) in self.aow_board.pieces[turn].items():
            if value == tuple(src):
                # # Update the location of the piece in the pieces array
                self.aow_board.pieces[turn][key] = tuple(dst)

        for (key, value) in self.aow_board.pieces[1 - turn].items():
            if value == (7 - dst[0], dst[1]):
                # Remove the location from the piece that was removed in the pieces array
                self.aow_board.pieces[1 - turn][key] = None

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
        if self.aow_board.is_piece(turn, Cell(current_row, current_col), Pieces.WARELEFANT):
            if current_row == next_row:
                start_col = min(current_col, next_col) + 1
                end_col = max(current_col, next_col)
                for col in range(start_col, end_col):
                    if self.aow_board.get_piece(Cell(current_row, col), turn) in [Pieces.PAWN, Pieces.HOPLITE]:
                        self.aow_board.set_piece(turn, Cell(current_row, col), Pieces.EMPTY)
                        self.aow_board.set_piece(1 - turn, Cell(7 - current_row, col), Pieces.EMPTY)
                        for key, value in self.aow_board.pieces[turn].items():
                            if value == (current_row, col):
                                self.aow_board.pieces[turn][key] = None
                        for key, value in self.aow_board.pieces[1 - turn].items():
                            if value == (7 - current_row, col):
                                self.aow_board.pieces[1 - turn][key] = None

            elif current_col == next_col:
                start_row = min(current_row, next_row) + 1
                end_row = max(current_row, next_row)
                for row in range(start_row, end_row):
                    if (self.aow_board.get_piece(Cell(row, current_col), turn) in [Pieces.PAWN, Pieces.HOPLITE] or
                            self.aow_board.get_piece(Cell(7 - row, current_col), 1 - turn) in [Pieces.PAWN, Pieces.HOPLITE]):
                        self.aow_board.set_piece(turn, Cell(row, current_col), Pieces.EMPTY)
                        self.aow_board.set_piece(1 - turn, Cell(7 - row, current_col), Pieces.EMPTY)
                        for key, value in self.aow_board.pieces[turn].items():
                            if value == (row, current_col):
                                self.aow_board.pieces[turn][key] = None
                        for key, value in self.aow_board.pieces[1 - turn].items():
                            if value == (7 - row, current_col):
                                self.aow_board.pieces[1 - turn][key] = None

    def is_game_done(self):
        return self.done or (self.steps >= self.max_steps)

    def promote_pawn_or_hoplite(self, pos: Cell, turn: int):
        if (self.aow_board.is_piece(turn, pos, Pieces.PAWN) or
                self.aow_board.is_piece(turn, pos, Pieces.HOPLITE)) and pos.row == 7:
            self.aow_board.set_piece(turn, pos, Pieces.QUEEN)

    def upgrade_piece(self, pos: Cell, turn: int, piece_to_upgrade: Pieces):
        rewards = [0, 0]
        rewards[turn] = Rewards.UPGRADE_PIECE
        rewards[1 - turn] = 0
        new_piece = Pieces.get_upgraded_variant(piece_to_upgrade)

        # get piece_name from position
        piece_name = None
        for key, value in self.aow_board.pieces[turn].items():
            if value == (pos.row, pos.col):
                piece_name = key
                break

        # return rewards if the piece is empty (This happens because of dutch waterline,
        # which can be activated on an empty space)
        if new_piece == Pieces.EMPTY or piece_name is None:
            return [0, 0], [set(), set()]

        split_piece_name = piece_name.split("_")

        if len(split_piece_name) < 2:
            return [0, 0], [set(), set()]

        # update the piece
        self.aow_board.pieces[turn][f"{Pieces.get_piece_name(new_piece).lower()}_{piece_name.split('_')[1]}"] = \
            self.aow_board.pieces[
                turn].pop(piece_name)
        self.aow_board.set_piece(turn, pos, new_piece)
        self.remove_resources(turn, new_piece)
        return rewards, [set(), set()]

    def remove_resources(self, turn: int, piece: Pieces):
        match piece:
            case Pieces.HOPLITE:
                self.aow_board.remove_resources(turn, 2)
            case Pieces.WINGED_KNIGHT:
                self.aow_board.remove_resources(turn, 3)
            case Pieces.WARELEFANT:
                self.aow_board.remove_resources(turn, 5)

    def step(self, action: int) -> tuple[list[int], bool, list[set]]:
        assert not self.is_game_done(), "the game is finished reset"
        assert action < self.action_space_length, f"action number must be less than {self.action_space_length}."

        source_pos, possibles, actions_mask = self.get_all_actions(self.turn)
        assert actions_mask[action], f"Cannot Take This Action = {action}, {source_pos[action]} -> {possibles[action]}"

        from_pos = Cell(int(source_pos[action][0]), int(source_pos[action][1]))
        next_pos = Cell(int(possibles[action][0]), int(possibles[action][1]))

        if from_pos == next_pos:
            source_pos_piece = self.aow_board.get_piece(Cell(from_pos[0], from_pos[1]), self.turn)
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
            rewards = self.add_reward(reward=Rewards.DUTCH_WATERLINE, turn=self.turn)
            end_turn = False

        rewards, infos = self.update_checks(rewards, infos)
        rewards, infos = self.update_check_mates(rewards, infos)
        rewards, infos = self.update_draw(rewards, infos)

        if from_pos != next_pos or end_turn:
            self.aow_board.add_resources(self.turn, 1)
            self.turn = 1 - self.turn
        self.steps += 1
        return rewards, self.is_game_done(), infos
