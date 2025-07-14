"""
Tests for the main application module.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import sys

from src.main import CanvusLLMInterface
from src.exceptions import CanvusLLMException, ConfigurationError


class TestCanvusLLMInterface:
    """Test the main application class."""
    
    def test_initialization(self):
        """Test basic initialization."""
        app = CanvusLLMInterface()
        assert app.config is not None
        assert app.tray is None
        assert app.is_running is False
        assert app.status == "Idle"
    
    def test_configuration_loading(self):
        """Test configuration loading."""
        app = CanvusLLMInterface()
        assert app.config is not None
        assert hasattr(app.config, 'canvus_server_url')
        assert hasattr(app.config, 'ollama_model')
    
    @pytest.mark.asyncio
    async def test_initialization_async(self):
        """Test async initialization."""
        app = CanvusLLMInterface()
        
        # Mock the tray to avoid actual system tray creation
        with patch('src.main.CanvusTray') as mock_tray:
            mock_tray_instance = mock_tray.return_value
            mock_tray_instance.start_tray.return_value = None
            
            # Mock configuration validation with async mocks
            with patch.object(app.config, 'test_canvus_connection', new_callable=AsyncMock) as mock_canvus:
                mock_canvus.return_value = True
                with patch.object(app.config, 'test_ollama_connection', new_callable=AsyncMock) as mock_ollama:
                    mock_ollama.return_value = True
                    with patch.object(app.config, 'validate_ollama_model', new_callable=AsyncMock) as mock_model:
                        mock_model.return_value = True
                        
                        # Mock client initialization
                        with patch.object(app, '_initialize_clients') as mock_clients:
                            mock_clients.return_value = None
                            
                            # Mock processing initialization
                            with patch.object(app, '_initialize_processing') as mock_processing:
                                mock_processing.return_value = None
                                
                                await app.initialize()
                                
                                assert app.is_running is True
                                mock_tray.assert_called_once()
    
    def test_restart_method(self):
        """Test restart method."""
        app = CanvusLLMInterface()
        
        # Test that restart calls sys.exit
        with pytest.raises(SystemExit) as exc_info:
            app.restart()
        
        assert exc_info.value.code == 0
    
    def test_get_status(self):
        """Test status reporting."""
        app = CanvusLLMInterface()
        
        # Test default status
        status = app.get_status()
        assert "Idle" in status
        
        # Test with connection status
        app.connection_status["canvus"] = True
        app.connection_status["ollama"] = False
        status = app.get_status()
        assert "Canvus: ✓" in status
        assert "Ollama: ✗" in status
    
    def test_update_status(self):
        """Test status updates."""
        app = CanvusLLMInterface()
        
        app.update_status("Testing")
        assert app.status == "Testing"
    
    @pytest.mark.asyncio
    async def test_validate_configuration_success(self):
        """Test successful configuration validation."""
        app = CanvusLLMInterface()
        
        # Mock successful connection tests
        with patch.object(app.config, 'test_canvus_connection', new_callable=AsyncMock) as mock_canvus:
            mock_canvus.return_value = True
            with patch.object(app.config, 'test_ollama_connection', new_callable=AsyncMock) as mock_ollama:
                mock_ollama.return_value = True
                with patch.object(app.config, 'validate_ollama_model', new_callable=AsyncMock) as mock_model:
                    mock_model.return_value = True
                    
                    await app._validate_configuration()
                    
                    assert app.connection_status["canvus"] is True
                    assert app.connection_status["ollama"] is True
    
    @pytest.mark.asyncio
    async def test_validate_configuration_failure(self):
        """Test configuration validation failure."""
        app = CanvusLLMInterface()
        
        # Mock failed connection tests
        with patch.object(app.config, 'test_canvus_connection', new_callable=AsyncMock) as mock_canvus:
            mock_canvus.return_value = False
            with patch.object(app.config, 'test_ollama_connection', new_callable=AsyncMock) as mock_ollama:
                mock_ollama.return_value = False
                with patch.object(app.config, 'validate_ollama_model', new_callable=AsyncMock) as mock_model:
                    mock_model.return_value = False
                    
                    await app._validate_configuration()
                    
                    assert app.connection_status["canvus"] is False
                    assert app.connection_status["ollama"] is False 