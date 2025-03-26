"""
Date Utility Module

This module provides utility functions for date calculations, such as 
retrieving a date from a specified number of days, months, or years ago.
"""

from datetime import datetime, timedelta

def get_past_date(days: int = 0, month: int = 0, year: int = 0) -> str:
    """
    Get the date from the specified number of days, months, or years ago.

    The function calculates a past date by first subtracting the specified 
    number of days, months, and years from today's date. If more than 30 days 
    are subtracted, the resulting date is set to the first day of that month.

    :param days: Number of days ago (default is 0)
    :type days: int, optional
    :param month: Number of months ago (default is 0)
    :type month: int, optional
    :param year: Number of years ago (default is 0)
    :type year: int, optional
    :return: The calculated past date in MM/DD/YYYY format
    :rtype: str

    **Examples:**

    >>> from datetime import datetime
    >>> past_date = get_past_date(days=60)
    >>> past_date
    '01/01/2025'

    >>> past_date = get_past_date(month=2)
    >>> past_date
    '01/01/2025'

    >>> past_date = get_past_date(year=1)
    >>> past_date
    '01/01/2024'
    """
    today = datetime.today()
    past_date = today - timedelta(days=days)  # Subtract days first
    past_date = past_date.replace(year=past_date.year - year)  # Subtract years
    if month:
        new_month = past_date.month - month
        while new_month <= 0:
            past_date = past_date.replace(year=past_date.year - 1)
            new_month += 12
        past_date = past_date.replace(month=new_month)
    
    # Only change to the first day if days >= 30
    if days >= 30 or month or year:
        past_date = past_date.replace(day=1)
    
    return past_date.strftime('%m/%d/%Y')


if __name__ == "__main__":
    print(get_past_date(days=2))
    print(get_past_date(days=60))
    print(get_past_date(month=3))
    print(get_past_date(year=2))
