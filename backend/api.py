from fastapi import FastAPI, HTTPException

from learnings.ppo import PPO
from utils import convert_move_to_positions, validate_board_size, raise_http_exception
from apimodels.requests import MoveRequest, AIGameRequest
from apimodels.responses import MoveResponse, InitializeResponse, AIGameResponse
from agents import PPOChess
from buffer.episode import Episode
from chess import Chess
import numpy as np
import sys
import logging
import pygame

WHITE_PPO_PATH = 'results/DoubleAgentsPPO/white_dict.pt'
BLACK_PPO_PATH = 'results/DoubleAgentsPPO/black_dict.pt'

app = FastAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename='api.log', format='%(asctime)s|%(name)s:%(levelname)s - %(message)s')
logger.info("API started.")

sys.setrecursionlimit(300)
env = Chess(window_size=800)

ppo = PPO(
    env,
    hidden_layers=(2048,) * 4,
    epochs=100,
    buffer_size=32 * 2,
    batch_size=128,
)

episode = Episode()
ppo_chess = PPOChess(env, ppo, 1, 32, "", WHITE_PPO_PATH, BLACK_PPO_PATH)


@app.get("/initialize", status_code=201)
def initialize():
    logger.info("Received initialize request.")
    try:
        env.reset()
        init_response = InitializeResponse(board=env.board.tolist(), cards=[], resources=0, pieces=env.pieces)

        logger.info("Initialized game")
        return init_response
    except FileNotFoundError as e:
        logger.error(f"Could not find model on specified location, make sure the location is correct. {e}")
        raise HTTPException(status_code=500, detail="Could not find any model.")
    except Exception as e:
        logger.error(f"An error occurred while resetting the game. {e}")
        raise HTTPException(status_code=500, detail="An error occurred while initializing the game.")

@app.post("/aigame", status_code=201)
def aigame(aigame_request: AIGameRequest):
    logger.info(f"Received aigame request: {aigame_request}")
    response = AIGameResponse(game=[], statistics=[])
    try:       
        match aigame_request.white_model.capitalize():
            case "PPO":
                white_model = WHITE_PPO_PATH
            case _:
                white_model = WHITE_PPO_PATH
                
        match aigame_request.black_model.capitalize():
            case "PPO":
                black_model = BLACK_PPO_PATH
            case _:
                black_model = BLACK_PPO_PATH    
                
        env = Chess(window_size=800)

        ppo = PPO(
            env,
            hidden_layers=(2048,) * 4,
            epochs=100,
            buffer_size=32 * 2,
            batch_size=128,
        )           
        
        ppo_chess = PPOChess(env, ppo, 1, 32, "", white_model, black_model)
        episode = Episode()
        logger.info("Initialized AI game.")
        
        # Play the game
        counter = 0
        states = []

        response.game.append(ppo_chess.env.get_state(ppo_chess.env.turn).tolist())
        
        while True:
            done, _ = ppo_chess.take_action(ppo_chess.env.turn, episode)
            response.game.append(ppo_chess.env.get_state(ppo_chess.env.turn).tolist())
            
            # print("turn: ", chess_game.env.turn)
            # env.render()
            counter += 1
            if done:
                #GameStates | Win -1 of 1 | nr turns | nr checks
                data = {'States': states, 'Win': ppo_chess.env.turn, 'Turns': counter}  
                #mydict.append(data)

                print("Game Over")
                print("Winner: White" if ppo_chess.env.turn else "Winner: Black")
                print("Game Length: ", counter)
                break
        
        logger.info(f"AI game completed.")
        return response
    except FileNotFoundError as e:
        logger.error(f"Could not find model on specified location, make sure the location is correct. {e}")
        raise HTTPException(status_code=500, detail="Could not find any model.")
    except Exception as e:
        logger.error(f"An error occurred while resetting the game. {e}")
        raise HTTPException(status_code=500, detail="An error occurred while initializing the game.")

@app.post("/move")
def move(move_request: MoveRequest):
    logger.info(f"Received move request: {move_request}")
    if ppo_chess is None:
        logger.error("No game has been initialized yet.")
        raise_http_exception(404, "No game has been initialized yet.")

    board: np.ndarray | None = None
    try:
        board = np.array(move_request.board)
        if not board.any():
            raise_http_exception(400, "Please provide a board.")
    except Exception as e:
        logger.warning(f"An error occurred while processing the board. {e}")
        raise_http_exception(400, "Invalid board.")

    validate_board_size(board, logger)

    env.set_board(board)
    env.turn = move_request.turn
    action_str = move_request.move

    try:
        # - TODO: Check error's thrown and make handling those better
        from_pos, to_pos = convert_move_to_positions(action_str)
        src, dst, _ = env.get_all_actions(env.turn)
        action = np.nonzero((src == from_pos).all(axis=1) & (dst == to_pos).all(axis=1))[0]
        if len(action) == 0:
            raise_http_exception(400, "Invalid move.")
        env.step(int(action[0]))
    except HTTPException as e:
        logger.warning(f"An error occurred while processing the move. {e}")
        raise e
    except Exception as e:
        logger.warning("Something went wrong while processing the move." + str(e))
        raise_http_exception(400, "Invalid move")

    try:
        ppo_chess.take_action(env.turn, episode)
    except Exception as e:
        logger.error(f"An error occurred while processing the AI's move. {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the AI's move.")

    logger.info("Move processed successfully.")
    return MoveResponse(board=env.board.tolist(), cards=[], resources=0, has_game_ended=env.done)
