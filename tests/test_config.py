"""
Tests for the configuration module.
"""

import pytest
from pathlib import Path

from src.config import Config


class TestConfig:
    """Test cases for the Config class."""
    
    def test_config_defaults(self):
        """Test that default configuration values are set correctly."""
        config = Config()
        assert str(config.canvus_server_url) == "http://localhost:3000/"
        assert config.canvus_api_key is None
        assert config.canvus_username is None
        assert config.canvus_password is None
        assert config.ollama_server_url == "http://localhost:11434"
        assert config.ollama_model == "gemma3"
        assert config.log_level == "INFO"
        assert config.max_retries == 3
        assert config.retry_delay == 10
        assert config.debug is False
        assert config.test_mode is False
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Test valid log level
        config = Config(log_level="DEBUG")
        assert config.log_level == "DEBUG"
        
        # Test invalid log level
        with pytest.raises(ValueError):
            Config(log_level="INVALID")
        
        # Test valid retry settings
        config = Config(max_retries=5, retry_delay=30)
        assert config.max_retries == 5
        assert config.retry_delay == 30
        
        # Test invalid retry settings
        with pytest.raises(ValueError):
            Config(max_retries=15)  # Too high
        
        with pytest.raises(ValueError):
            Config(retry_delay=0)  # Too low
    
    def test_authentication_methods(self):
        """Test authentication method detection."""
        # No credentials
        config = Config()
        assert config.get_auth_method() == "none"
        assert not config.is_authenticated()
        
        # API key
        config = Config(canvus_api_key="test_key")
        assert config.get_auth_method() == "api_key"
        assert config.is_authenticated()
        
        # Username/password
        config = Config(canvus_username="user", canvus_password="pass")
        assert config.get_auth_method() == "username_password"
        assert config.is_authenticated()
    
    def test_config_file_path(self):
        """Test configuration file path generation."""
        config = Config()
        config_path = config.get_config_file_path()
        
        assert isinstance(config_path, Path)
        assert "CanvusLLM" in str(config_path)
        assert config_path.name == "config.json"
    
    def test_config_serialization(self):
        """Test configuration serialization and deserialization."""
        # Create a test configuration
        test_config = Config(
            canvus_server_url="http://test:3000",
            canvus_api_key="test_key",
            ollama_model="test_model"
        )
        
        # Save configuration
        test_config.save_config()
        
        # Load configuration
        loaded_config = Config.load_config()
        
        # Verify loaded configuration
        assert str(loaded_config.canvus_server_url) == "http://test:3000/"
        assert loaded_config.canvus_api_key == "test_key"
        assert loaded_config.ollama_model == "test_model" 