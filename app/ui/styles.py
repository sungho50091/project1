"""
Design system and styling constants for the Study Planner App.

Defines colors, fonts, spacing, and other design tokens.
"""

import flet as ft

# Colors
class Colors:
    """Color palette for the application."""
    PRIMARY = "#1976D2"  # Blue
    SECONDARY = "#81C784"  # Green
    ACCENT = "#FF9800"  # Orange
    
    SUCCESS = "#4CAF50"
    WARNING = "#FFC107"
    ERROR = "#F44336"
    
    BACKGROUND = "#FAFAFA"
    SURFACE = "#FFFFFF"
    
    TEXT_PRIMARY = "#212121"
    TEXT_SECONDARY = "#757575"
    TEXT_DISABLED = "#BDBDBD"
    
    # Priority colors
    PRIORITY_HIGH = "#F44336"  # Red
    PRIORITY_MEDIUM = "#FF9800"  # Orange
    PRIORITY_LOW = "#4CAF50"  # Green


# Typography
class FontSizes:
    """Font sizes for the application."""
    HEADLINE_LARGE = 32
    HEADLINE_MEDIUM = 28
    HEADLINE_SMALL = 24
    
    TITLE_LARGE = 22
    TITLE_MEDIUM = 16
    TITLE_SMALL = 14
    
    BODY_LARGE = 16
    BODY_MEDIUM = 14
    BODY_SMALL = 12
    
    LABEL_LARGE = 14
    LABEL_MEDIUM = 12
    LABEL_SMALL = 11


class FontWeights:
    """Font weights for the application."""
    THIN = 100
    EXTRA_LIGHT = 200
    LIGHT = 300
    NORMAL = 400
    MEDIUM = 500
    SEMI_BOLD = 600
    BOLD = 700
    EXTRA_BOLD = 800
    BLACK = 900


# Spacing
class Spacing:
    """Spacing units (in pixels)."""
    EXTRA_SMALL = 4
    SMALL = 8
    MEDIUM = 16
    LARGE = 24
    EXTRA_LARGE = 32


# Border Radius
class BorderRadius:
    """Border radius values."""
    SMALL = 4
    MEDIUM = 8
    LARGE = 12
    EXTRA_LARGE = 16
    ROUND = 50


# Shadow
class Shadow:
    """Shadow elevation values."""
    ELEVATION_0 = 0
    ELEVATION_1 = 1
    ELEVATION_2 = 2
    ELEVATION_3 = 3
    ELEVATION_4 = 4


def get_priority_color(priority: str) -> str:
    """
    Get color based on priority level.
    
    Args:
        priority: Priority level ('high', 'medium', 'low')
    
    Returns:
        Hex color code
    """
    priority_map = {
        "high": Colors.PRIORITY_HIGH,
        "medium": Colors.PRIORITY_MEDIUM,
        "low": Colors.PRIORITY_LOW,
    }
    return priority_map.get(priority.lower(), Colors.PRIMARY)
