"""
Custom exceptions for AeroSDK.
"""


class AeroSDKError(Exception):
    """Base exception for all AeroSDK errors."""
    pass


class ConnectionError(AeroSDKError):
    """Raised when unable to connect to the backend."""
    pass


class ValidationError(AeroSDKError):
    """Raised when data validation fails."""
    pass


class NotFoundError(AeroSDKError):
    """Raised when a resource is not found."""
    pass


class ServerError(AeroSDKError):
    """Raised when server returns an error."""
    pass
