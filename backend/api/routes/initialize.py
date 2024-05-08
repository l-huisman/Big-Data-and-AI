import logging

from api.models.responses import InitializeResponse
from utils import raise_http_exception

logger = logging.getLogger(__name__)


def initialize(env):
    logger.info("Received initialize request.")
    try:
        env.reset()
        return InitializeResponse(board=env.board.tolist(), cards=[], resources=0, pieces=env.pieces)
    except FileNotFoundError as e:
        logger.error(f"Could not find model on specified location, make sure the location is correct. {e}")
        raise raise_http_exception(status_code=500, detail="Could not find any model.")
    except Exception as e:
        logger.error(f"An error occurred while resetting the game. {e}")
        raise raise_http_exception(status_code=500, detail="An error occurred while initializing the game.")
    finally:
        logger.info("Initialized game.")
