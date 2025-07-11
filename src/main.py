"""
Main application module for the Canvus-Local-LLM interface.

This module contains the main application class that orchestrates all components
including the system tray interface, configuration management, and processing workflows.
"""

import asyncio
import sys
from typing import Optional

from loguru import logger

from .config import Config
from .exceptions import CanvusLLMException, ConfigurationError


class CanvusLLMInterface:
    """
    Main application class for the Canvus-Local-LLM interface.
    
    This class manages the system tray application, configuration,
    and all processing workflows.
    """
    
    def __init__(self):
        """Initialize the application."""
        self.config: Optional[Config] = None
        self.tray_icon = None
        self.canvus_client = None
        self.ollama_client = None
        self.processing_queue = asyncio.Queue()
        self.active_subscriptions = {}
        self.is_running = False
        
        # Initialize logging
        self._setup_logging()
        
        # Load configuration
        self._load_configuration()
    
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        logger.remove()  # Remove default handler
        
        # Add console handler
        logger.add(
            sys.stderr,
            level=self.config.log_level if self.config else "INFO",
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                   "<level>{message}</level>"
        )
        
        # Add file handler
        logger.add(
            "logs/canvus_llm.log",
            rotation="10 MB",
            retention="7 days",
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
        )
        
        logger.info("Logging initialized")
    
    def _load_configuration(self) -> None:
        """Load application configuration."""
        try:
            self.config = Config.load_config()
            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise ConfigurationError(f"Configuration loading failed: {e}")
    
    async def initialize(self) -> None:
        """Initialize the application components."""
        try:
            logger.info("Initializing Canvus-Local-LLM application")
            
            # Validate configuration
            self._validate_configuration()
            
            # Initialize system tray
            await self._initialize_system_tray()
            
            # Initialize API clients
            await self._initialize_clients()
            
            # Initialize processing components
            await self._initialize_processing()
            
            self.is_running = True
            logger.info("Application initialized successfully")
            
        except Exception as e:
            logger.error(f"Application initialization failed: {e}")
            raise CanvusLLMException(f"Initialization failed: {e}")
    
    def _validate_configuration(self) -> None:
        """Validate the loaded configuration."""
        if not self.config:
            raise ConfigurationError("No configuration loaded")
        
        if not self.config.is_authenticated():
            raise ConfigurationError("No authentication credentials provided")
        
        logger.info(f"Configuration validated - Auth method: {self.config.get_auth_method()}")
    
    async def _initialize_system_tray(self) -> None:
        """Initialize the system tray interface."""
        # TODO: Implement system tray initialization
        logger.info("System tray initialization placeholder")
    
    async def _initialize_clients(self) -> None:
        """Initialize API clients."""
        # TODO: Initialize Canvus client
        # TODO: Initialize Ollama client
        logger.info("API clients initialization placeholder")
    
    async def _initialize_processing(self) -> None:
        """Initialize processing components."""
        # TODO: Initialize processing queue
        # TODO: Initialize subscription managers
        logger.info("Processing components initialization placeholder")
    
    async def start(self) -> None:
        """Start the application."""
        try:
            await self.initialize()
            logger.info("Application started successfully")
            
            # Keep the application running
            while self.is_running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.error(f"Application error: {e}")
            raise
        finally:
            await self.shutdown()
    
    async def shutdown(self) -> None:
        """Shutdown the application gracefully."""
        try:
            logger.info("Shutting down application")
            
            self.is_running = False
            
            # Shutdown processing components
            await self._shutdown_processing()
            
            # Shutdown API clients
            await self._shutdown_clients()
            
            # Shutdown system tray
            await self._shutdown_system_tray()
            
            logger.info("Application shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    
    async def _shutdown_processing(self) -> None:
        """Shutdown processing components."""
        # TODO: Implement processing shutdown
        logger.info("Processing components shutdown placeholder")
    
    async def _shutdown_clients(self) -> None:
        """Shutdown API clients."""
        # TODO: Implement client shutdown
        logger.info("API clients shutdown placeholder")
    
    async def _shutdown_system_tray(self) -> None:
        """Shutdown system tray interface."""
        # TODO: Implement system tray shutdown
        logger.info("System tray shutdown placeholder")
    
    def restart(self) -> None:
        """Restart the application."""
        logger.info("Restarting application")
        # TODO: Implement restart logic
        pass


async def main():
    """Main entry point for the application."""
    app = CanvusLLMInterface()
    await app.start()


if __name__ == "__main__":
    asyncio.run(main()) 