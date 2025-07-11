"""
Configuration management for the Canvus-Local-LLM application.

This module handles all configuration settings including Canvus server connection,
Ollama model settings, and application preferences.
"""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application configuration settings."""
    
    # Canvus Server Configuration
    canvus_server_url: str = Field(
        default="http://localhost:3000",
        description="Canvus server URL"
    )
    canvus_api_key: Optional[str] = Field(
        default=None,
        description="Canvus API key for authentication"
    )
    canvus_username: Optional[str] = Field(
        default=None,
        description="Canvus username for authentication"
    )
    canvus_password: Optional[str] = Field(
        default=None,
        description="Canvus password for authentication"
    )
    
    # Ollama Configuration
    ollama_server_url: str = Field(
        default="http://localhost:11434",
        description="Ollama server URL"
    )
    ollama_model: str = Field(
        default="gemma3",
        description="Ollama model to use for AI processing"
    )
    
    # Application Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    max_retries: int = Field(
        default=3,
        description="Maximum number of retry attempts"
    )
    retry_delay: int = Field(
        default=10,
        description="Delay between retry attempts in seconds"
    )
    
    # Development Configuration
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    test_mode: bool = Field(
        default=False,
        description="Enable test mode"
    )
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }
    
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the allowed values."""
        allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed_levels:
            raise ValueError(f"Log level must be one of: {allowed_levels}")
        return v.upper()
    
    @field_validator("max_retries")
    @classmethod
    def validate_max_retries(cls, v: int) -> int:
        """Validate max retries is within reasonable bounds."""
        if v < 0 or v > 10:
            raise ValueError("Max retries must be between 0 and 10")
        return v
    
    @field_validator("retry_delay")
    @classmethod
    def validate_retry_delay(cls, v: int) -> int:
        """Validate retry delay is within reasonable bounds."""
        if v < 1 or v > 300:
            raise ValueError("Retry delay must be between 1 and 300 seconds")
        return v
    
    def get_config_file_path(self) -> Path:
        """Get the configuration file path."""
        app_data = Path(os.getenv("APPDATA", ""))
        config_dir = app_data / "CanvusLLM"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "config.json"
    
    def save_config(self) -> None:
        """Save configuration to file."""
        config_path = self.get_config_file_path()
        with open(config_path, "w") as f:
            f.write(self.model_dump_json(indent=2))
    
    @classmethod
    def load_config(cls) -> "Config":
        """Load configuration from file."""
        config_path = cls().get_config_file_path()
        if config_path.exists():
            with open(config_path, "r") as f:
                config_data = f.read()
                return cls.model_validate_json(config_data)
        return cls()
    
    def is_authenticated(self) -> bool:
        """Check if authentication credentials are available."""
        return bool(self.canvus_api_key or (self.canvus_username and self.canvus_password))
    
    def get_auth_method(self) -> str:
        """Get the authentication method being used."""
        if self.canvus_api_key:
            return "api_key"
        elif self.canvus_username and self.canvus_password:
            return "username_password"
        return "none" 