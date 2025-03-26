"""
Logger Setup Module

This module provides functionality for setting up a logger with both console and file handlers.
It allows customization of log levels and formats for improved logging in automation scripts.

Functions:
    - setup_logger: Configures and returns a logger instance.

Example Usage:
    ```python
    logger = setup_logger()
    logger.info("This is an info message")
    ```
"""

import logging


def setup_logger(
    log_file=r"./logs/logfile.log", log_level_console=logging.ERROR, log_level_file=logging.INFO
):
    """
    Sets up a logger with console and file handlers.

    :param log_file: Path to the log file.
    :type log_file: str
    :param log_level_console: Logging level for console output.
    :type log_level_console: int
    :param log_level_file: Logging level for file output.
    :type log_level_file: int
    :return: Configured logger instance.
    :rtype: logging.Logger
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    console_formatter = logging.Formatter("%(asctime)s: %(message)s")
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level_console)
    console_handler.setFormatter(console_formatter)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level_file)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    # Example usage
    import os
    import sys
    
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from utils.file_folder import create_directories

    create_directories([os.path.join(os.getcwd(), "logs"),])

    logger = setup_logger()
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
