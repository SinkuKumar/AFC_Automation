import logging

def setup_logger(
    log_file="logfile.log", log_level_console=logging.ERROR, log_level_file=logging.INFO
):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    console_formatter = logging.Formatter("%(asctime)s: %(message)s")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level_console)
    console_handler.setFormatter(console_formatter)

    file_handler = logging.FileHandler(os.path.join("logs", log_file))
    file_handler.setLevel(log_level_file)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Example usage
if __name__ == "__main__":
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
