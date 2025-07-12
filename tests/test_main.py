"""
Tests for the main application module.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock

from src.main import CanvusLLMInterface
from src.exceptions import ConfigurationError


class TestCanvusLLMInterface:
    """Test cases for the main application class."""
    
    def test_initialization(self):
        """Test that the application can be initialized."""
        with patch('src.main.Config.load_config') as mock_load_config:
            mock_config = MagicMock()
            mock_config.log_level = "INFO"
            mock_config.is_authenticated.return_value = True
            mock_config.get_auth_method.return_value = "api_key"
            mock_load_config.return_value = mock_config
            
            app = CanvusLLMInterface()
            assert app is not None
            assert app.config is not None
            assert app.is_running is False
    
    def test_configuration_loading(self):
        """Test configuration loading."""
        with patch('src.main.Config.load_config') as mock_load_config:
            mock_config = MagicMock()
            mock_config.log_level = "INFO"
            mock_config.is_authenticated.return_value = True
            mock_config.get_auth_method.return_value = "api_key"
            mock_load_config.return_value = mock_config
            
            app = CanvusLLMInterface()
            assert app.config is not None
    
    @pytest.mark.asyncio
    async def test_initialization_async(self):
        """Test async initialization."""
        with patch('src.main.Config.load_config') as mock_load_config:
            mock_config = MagicMock()
            mock_config.log_level = "INFO"
            mock_config.is_authenticated.return_value = True
            mock_config.get_auth_method.return_value = "api_key"
            mock_load_config.return_value = mock_config
            
            app = CanvusLLMInterface()
            await app.initialize()
            assert app.is_running is True
    
    def test_restart_method(self):
        """Test restart method exists."""
        with patch('src.main.Config.load_config') as mock_load_config:
            mock_config = MagicMock()
            mock_config.log_level = "INFO"
            mock_config.is_authenticated.return_value = True
            mock_config.get_auth_method.return_value = "api_key"
            mock_load_config.return_value = mock_config
            
            app = CanvusLLMInterface()
            # Should not raise an exception
            app.restart() 