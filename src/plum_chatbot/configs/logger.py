import logging
import os

from plum_chatbot.configs.folders import LOGS_DIR


def setup_global_logging() -> None:
    """
    Setup global logging configuration that applies to all loggers.
    This should be called once during application startup.
    """
    os.makedirs(LOGS_DIR, exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove any existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Add file handler
    log_file = LOGS_DIR / "application.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)

    # Add console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)

    # Prevent propagation issues
    root_logger.propagate = False


def setup_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    Uses the global logging configuration set by setup_global_logging().
    """
    return logging.getLogger(name)
