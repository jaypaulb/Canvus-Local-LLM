"""
Custom exception classes for the Canvus-Local-LLM application.

This module defines all custom exceptions used throughout the application
for proper error handling and debugging.
"""

from typing import Any, Dict, Optional


class CanvusLLMException(Exception):
    """Base exception for all Canvus-Local-LLM application errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConfigurationError(CanvusLLMException):
    """Raised when there are configuration-related errors."""
    pass


class AuthenticationError(CanvusLLMException):
    """Raised when authentication fails."""
    pass


class ConnectionError(CanvusLLMException):
    """Raised when connection to external services fails."""
    pass


class CanvusAPIError(CanvusLLMException):
    """Raised when Canvus API operations fail."""
    pass


class OllamaError(CanvusLLMException):
    """Raised when Ollama operations fail."""
    pass


class ProcessingError(CanvusLLMException):
    """Raised when AI processing operations fail."""
    pass


class ValidationError(CanvusLLMException):
    """Raised when data validation fails."""
    pass


class FileError(CanvusLLMException):
    """Raised when file operations fail."""
    pass


class ModelError(CanvusLLMException):
    """Raised when model-related operations fail."""
    pass


class SubscriptionError(CanvusLLMException):
    """Raised when subscription stream operations fail."""
    pass


class WorkflowError(CanvusLLMException):
    """Raised when workflow processing fails."""
    pass


class RetryExhaustedError(CanvusLLMException):
    """Raised when all retry attempts have been exhausted."""
    pass


class TimeoutError(CanvusLLMException):
    """Raised when operations timeout."""
    pass


class ResourceError(CanvusLLMException):
    """Raised when resource limits are exceeded."""
    pass 