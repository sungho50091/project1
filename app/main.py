"""
Main entry point for the Study Planner App.

This module initializes the Flet application and sets up the UI.
"""

import sys
from pathlib import Path

import flet as ft

from app.ui.screens import create_home_screen
from config.settings import get_settings
from utils.logger import setup_logger

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logger = setup_logger(__name__)
settings = get_settings()


def create_app():
    """
    Create and configure the main Flet application.
    
    Returns:
        flet.Page: Configured Flet page object
    """
    def main(page: ft.Page) -> None:
        """Main application entry point."""
        page.title = "📚 Study Planner"
        page.window_width = 400
        page.window_height = 800
        page.window_min_width = 300
        page.window_min_height = 600
        page.theme_mode = ft.ThemeMode.LIGHT
        
        # Set up color scheme
        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=ft.colors.BLUE,
                secondary=ft.colors.LIGHT_BLUE,
            )
        )
        
        logger.info("Application started")
        
        # Create home screen
        home_screen = create_home_screen(page)
        page.add(home_screen)
    
    return main


if __name__ == "__main__":
    logger.info("Initializing Study Planner App v%s", settings.app_version)
    app = create_app()
    ft.app(target=app)
