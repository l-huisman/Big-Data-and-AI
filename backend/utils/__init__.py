import numpy as np
import torch as T
import torch.nn as nn
import cv2
from fastapi import HTTPException

BOARD_LENGTH = 8
BOARD_WIDTH = 8
BOARD_SIDES = 2


def build_base_model(
        input_size: int,
        hidden_layers: tuple[int],
        output_size: int,
        last_activation: nn.Module = nn.Identity(),
) -> nn.Module:
    layers = [
        nn.Linear(input_size, hidden_layers[0]),
        nn.ReLU(),
    ]

    for i in range(len(hidden_layers) - 1):
        in_features = hidden_layers[i]
        out_features = hidden_layers[i + 1]
        layers += [
            nn.Linear(in_features, out_features),
            nn.ReLU(),
        ]

    layers += [nn.Linear(hidden_layers[-1], output_size), last_activation]

    return nn.Sequential(*layers)


def make_batch_ids(n: int, batch_size: int, shuffle: bool = True) -> np.ndarray:
    starts = np.arange(0, n, batch_size)
    indices = np.arange(n, dtype=np.int64)
    if shuffle:
        np.random.shuffle(indices)
    return [indices[i: i + batch_size] for i in starts]


def tensor_to_numpy(x: T.Tensor) -> np.ndarray:
    return x.detach().cpu().numpy()


def save_to_video(path: str, frames: np.ndarray, fps: int = 2):
    size = frames.shape[1:3]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(
        path,
        fourcc,
        fps,
        size,
    )
    for f in frames:
        out.write(f)
    out.release()


def raise_http_exception(status_code, detail):
    raise HTTPException(status_code=status_code, detail=detail)


def validate_board_size(board, logger=None):
    if len(board) != BOARD_SIDES:
        raise_http_exception(400, f"Invalid board size. ({len(board)}) should be {BOARD_SIDES}.")
    if len(board[0]) != BOARD_WIDTH or len(board[1]) != BOARD_WIDTH:
        raise_http_exception(400,
                             f"Invalid board size. ({len(board[0])}, {len(board[1])}) should be {BOARD_WIDTH}, {BOARD_WIDTH}")
    for row in board[0]:
        if len(row) != BOARD_LENGTH:
            raise_http_exception(400, f"Invalid board size. ({len(row)}) should be {BOARD_LENGTH}")
    for row in board[1]:
        if len(row) != BOARD_LENGTH:
            raise_http_exception(400, f"Invalid board size. ({len(row)}) should be {BOARD_LENGTH}")


def convert_move_to_positions(action_str):
    f1 = int(action_str[1]) - 1
    f2 = ord(action_str[0]) - ord('a')
    from_pos = np.array([f1, f2])
    f1 = int(action_str[3]) - 1
    f2 = ord(action_str[2]) - ord('a')
    to_pos = np.array([f1, f2])
    return from_pos, to_pos
