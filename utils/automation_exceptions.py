"""
Selenium Exception Module

This module defines a custom exception class for handling Selenium-related errors.
It ensures a clear error message is provided while suppressing the stack trace.

Modules:
    SeleniumException: Custom exception for Selenium errors.
"""

import os
import sys

# Adjust the system path to include the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import error_messages as em


class SeleniumException(Exception):
    """
    Custom exception for Selenium errors with suppressed stack trace.

    :param message: Error message associated with the exception.
    :type message: str
    """

    def __init__(self, message):
        """
        Initializes the SeleniumException with a message.

        :param message: Error message describing the exception.
        :type message: str
        """
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        """
        Returns the string representation of the exception.

        :return: The error message.
        :rtype: str
        """
        return self.message


if __name__ == "__main__":
    # Example usage
    try:
        raise SeleniumException("Browser crashed unexpectedly!")
    except SeleniumException as e:
        print(e)
