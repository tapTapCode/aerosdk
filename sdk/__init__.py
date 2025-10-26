"""
AeroSDK - Aerospace data processing SDK.
"""

from .client import AeroClient
from .models import (
    Component,
    ComponentCreate,
    ComponentUpdate,
    ComponentType,
    Assembly,
    FileUploadResponse,
)
from .exceptions import (
    AeroSDKError,
    ConnectionError,
    ValidationError,
    NotFoundError,
    ServerError,
)

__version__ = "0.1.0"
__all__ = [
    "AeroClient",
    "Component",
    "ComponentCreate",
    "ComponentUpdate",
    "ComponentType",
    "Assembly",
    "FileUploadResponse",
    "AeroSDKError",
    "ConnectionError",
    "ValidationError",
    "NotFoundError",
    "ServerError",
]
