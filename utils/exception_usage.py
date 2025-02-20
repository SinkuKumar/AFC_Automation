import os
import sys
import logging
import traceback

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import error_messages

# Configure logging
LOG_FILE = "error_log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, 
                    format="%(asctime)s - %(levelname)s - %(message)s")


class SeleniumException(Exception):
    """Custom exception for Selenium errors with suppressed stack trace."""
    
    def __init__(self, message):
        self.message = message + f" | Contact: {error_messages.CONTACT}"
        super().__init__(self.message)

    def __str__(self):
        return self.message

if __name__ == "__main__":
    # Example usage
    try:
        raise SeleniumException("Browser crashed unexpectedly!")
    except SeleniumException as e:
        logging.error("An error occurred:\n" + traceback.format_exc())
        print(e)
