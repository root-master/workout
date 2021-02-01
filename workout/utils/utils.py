"""
Utilities.
"""

from datetime import datetime

import pytz


def now():
    """Returns timestamp of PST timezone."""
    return datetime.now().astimezone(pytz.timezone("US/Pacific")).timestamp()


def date():
    """Returns today's date"""
    return datetime.now().astimezone(pytz.timezone("US/Pacific")).strftime("%Y-%m-%d")
