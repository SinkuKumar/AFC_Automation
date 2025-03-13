from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging

def get_current_date() -> str:
    """
    Get the current date in MM/DD/YYYY format.

    This function retrieves the current system date and returns it as a formatted string.

    Returns:
        str: The current date in MM/DD/YYYY format.

    Raises:
        Exception: If an unexpected error occurs while retrieving the date.
    """
    try:
        current_date = datetime.today().strftime("%m/%d/%Y")
        logging.info("Successfully retrieved the current date: %s", current_date)
        return current_date
    except Exception as e:
        logging.error("Error occurred while fetching current date: %s", str(e))
        raise

def get_yesterdays_date() -> str:
    """
    Returns yesterday's date in MM/DD/YYYY format.

    Args:
        None

    Returns:
        str: Yesterday's date in MM/DD/YYYY format.

    Raises:
        Exception: If an unexpected error occurs while retrieving the date.
    """
    try:
        yesterday = datetime.now() - timedelta(days=1)
        logging.info("Successfully retrieved the yesterday's date")
        return yesterday.strftime("%m/%d/%Y")
    except Exception as e:
        logging.error("Error occurred while fetching yesterday's date: %s", str(e))
        raise

def get_past_date(days: int = 0, months: int = 0, years: int = 0, quarters: int = 0, from_date: str = None) -> str:
    """
    Calculate a past date by subtracting the specified number of days, months, years, or quarters.

    This function computes a past date by subtracting the given time values from the provided
    `from_date` (or the current date if not specified).

    Args:
        days (int, optional): Number of days to subtract. Defaults to 0.
        months (int, optional): Number of months to subtract. Defaults to 0.
        years (int, optional): Number of years to subtract. Defaults to 0.
        quarters (int, optional): Number of quarters to subtract (1 quarter = 3 months). Defaults to 0.
        from_date (str, optional): The reference date in "MM/DD/YYYY" format. If not provided, uses the current date.

    Returns:
        str: The calculated past date in "MM/DD/YYYY" format.

    Raises:
        ValueError: If `from_date` is not in the correct "MM/DD/YYYY" format.
        Exception: If an unexpected error occurs.
    """
    try:
        if from_date:
            try:
                base_date = datetime.strptime(from_date, "%m/%d/%Y")
            except ValueError:
                logging.error("Invalid date format provided: %s. Expected format: MM/DD/YYYY.", from_date)
                raise ValueError("Invalid date format. Use MM/DD/YYYY.")
        else:
            base_date = datetime.today()

        past_date = base_date - relativedelta(days=days, months=months + (quarters * 3), years=years)
        past_date_str = past_date.strftime("%m/%d/%Y")
        return past_date_str

    except Exception as e:
        logging.error("Error occurred while calculating past date: %s", str(e))
        raise
