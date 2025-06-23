import logging
import os

from plum_chatbot.configs.folders import LOGS_DIR


def setup_logger(name: str) -> logging.Logger:
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_file = LOGS_DIR / f"{name}.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if setup_logger is called multiple times
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
