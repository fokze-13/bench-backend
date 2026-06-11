import logging
import sys
from app.config import LOGGING_FORMAT, LOGGING_DATE_FORMAT


def setup_logger(name: str, level: int) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter(LOGGING_FORMAT, datefmt=LOGGING_DATE_FORMAT)
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger
