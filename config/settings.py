"""
Application settings and configuration.

Uses environment variables and .env file.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import Field

# Project root
PROJECT_ROOT = Path(__file__).parent.parent


class Settings(BaseSettings):
    """
    Application settings.
    
    Reads from environment variables and .env file.
    """
    
    # App settings
    app_name: str = Field(default="Study Planner", env="APP_NAME")
    app_version: str = Field(default="0.1.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Database
    database_url: str = Field(default="sqlite:///data/database.db", env="DATABASE_URL")
    db_path: str = Field(default="data/database.db", env="DB_PATH")
    
    # OpenAI API
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4-turbo-preview", env="OPENAI_MODEL")
    openai_max_tokens: int = Field(default=2000, env="OPENAI_MAX_TOKENS")
    openai_temperature: float = Field(default=0.7, env="OPENAI_TEMPERATURE")
    
    # UI settings
    window_width: int = Field(default=400, env="WINDOW_WIDTH")
    window_height: int = Field(default=800, env="WINDOW_HEIGHT")
    theme_mode: str = Field(default="light", env="THEME_MODE")  # light or dark
    
    # Notification settings
    enable_notifications: bool = Field(default=True, env="ENABLE_NOTIFICATIONS")
    notification_lead_time_minutes: int = Field(
        default=30,
        env="NOTIFICATION_LEAD_TIME_MINUTES",
    )
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/app.log", env="LOG_FILE")
    
    class Config:
        """Pydantic config."""
        env_file = PROJECT_ROOT / "config" / ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Get settings singleton.
    
    Returns:
        Settings instance
    """
    return Settings()
