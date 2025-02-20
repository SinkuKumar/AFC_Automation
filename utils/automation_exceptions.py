import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import error_messages as em

class SeleniumException(Exception):
    """Custom exception for Selenium errors with suppressed stack trace."""
    
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

if __name__ == "__main__":
    # Example usage
    try:
        raise SeleniumException("Browser crashed unexpectedly!")
    except SeleniumException as e:
        print(e)