"""
Date and time utility functions.
"""

from datetime import datetime, timedelta
from typing import Optional


def format_date(date_obj: datetime, format_str: str = "%Y-%m-%d %H:%M") -> str:
    """
    Format datetime object to string.
    
    Args:
        date_obj: Datetime object
        format_str: Format string
    
    Returns:
        Formatted date string
    """
    return date_obj.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d %H:%M") -> Optional[datetime]:
    """
    Parse date string to datetime object.
    
    Args:
        date_str: Date string
        format_str: Format string
    
    Returns:
        Datetime object or None if parsing fails
    """
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        return None


def get_relative_date_str(date_obj: datetime) -> str:
    """
    Get a human-readable relative date string.
    
    Args:
        date_obj: Datetime object
    
    Returns:
        Relative date string (e.g., "in 2 days", "yesterday")
    """
    now = datetime.now()
    delta = date_obj - now
    
    if delta.days < 0:
        return "Overdue"
    elif delta.days == 0:
        return "Today"
    elif delta.days == 1:
        return "Tomorrow"
    elif delta.days <= 7:
        return f"In {delta.days} days"
    else:
        return date_obj.strftime("%m/%d")


def is_overdue(due_date: datetime) -> bool:
    """
    Check if a due date is overdue.
    
    Args:
        due_date: Due date
    
    Returns:
        True if overdue
    """
    return due_date < datetime.now()
