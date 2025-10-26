"""
AeroSDK Client - Main entry point for consuming the AeroSDK backend API.
"""

import httpx
from typing import List, Optional
from .models import Component, ComponentCreate, ComponentUpdate, ComponentType
from .exceptions import ConnectionError, NotFoundError, ServerError, ValidationError


class AeroClient:
    """
    Client for interacting with the AeroSDK backend.
    
    Usage:
        client = AeroClient("http://localhost:8000")
        components = client.get_components()
    """

    def __init__(self, base_url: str, timeout: float = 10.0):
        """
        Initialize the AeroClient.
        
        Args:
            base_url: The base URL of the backend API (e.g., "http://localhost:8000")
            timeout: Request timeout in seconds (default: 10.0)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.Client(base_url=self.base_url, timeout=timeout)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes the HTTP client."""
        self.close()

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def _handle_response(self, response: httpx.Response):
        """Handle HTTP responses and raise appropriate exceptions."""
        if response.status_code == 404:
            raise NotFoundError(response.text)
        elif response.status_code >= 500:
            raise ServerError(f"Server error: {response.text}")
        elif response.status_code >= 400:
            raise ValidationError(f"Validation error: {response.text}")
        response.raise_for_status()

    def get_components(self) -> List[Component]:
        """
        Get all components.
        
        Returns:
            List of Component objects
            
        Raises:
            ConnectionError: If unable to connect to the backend
            ServerError: If the server returns an error
        """
        try:
            response = self._client.get("/api/components")
            self._handle_response(response)
            return [Component(**item) for item in response.json()]
        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to {self.base_url}: {e}")

    def get_component(self, component_id: int) -> Component:
        """
        Get a specific component by ID.
        
        Args:
            component_id: The ID of the component
            
        Returns:
            Component object
            
        Raises:
            NotFoundError: If component not found
            ConnectionError: If unable to connect
        """
        try:
            response = self._client.get(f"/api/components/{component_id}")
            self._handle_response(response)
            return Component(**response.json())
        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to {self.base_url}: {e}")

    def create_component(self, component: ComponentCreate) -> Component:
        """
        Create a new component.
        
        Args:
            component: ComponentCreate object with component data
            
        Returns:
            Created Component object
            
        Raises:
            ValidationError: If data validation fails
            ConnectionError: If unable to connect
        """
        try:
            response = self._client.post(
                "/api/components",
                json=component.model_dump()
            )
            self._handle_response(response)
            return Component(**response.json())
        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to {self.base_url}: {e}")

    def update_component(
        self, component_id: int, component: ComponentUpdate
    ) -> Component:
        """
        Update a component.
        
        Args:
            component_id: The ID of the component to update
            component: ComponentUpdate object with updated fields
            
        Returns:
            Updated Component object
            
        Raises:
            NotFoundError: If component not found
            ValidationError: If data validation fails
            ConnectionError: If unable to connect
        """
        try:
            response = self._client.put(
                f"/api/components/{component_id}",
                json=component.model_dump(exclude_none=True)
            )
            self._handle_response(response)
            return Component(**response.json())
        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to {self.base_url}: {e}")

    def delete_component(self, component_id: int) -> None:
        """
        Delete a component.
        
        Args:
            component_id: The ID of the component to delete
            
        Raises:
            NotFoundError: If component not found
            ConnectionError: If unable to connect
        """
        try:
            response = self._client.delete(f"/api/components/{component_id}")
            self._handle_response(response)
        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to {self.base_url}: {e}")

    def filter_components(
        self, component_type: Optional[ComponentType] = None
    ) -> List[Component]:
        """
        Filter components by type.
        
        Args:
            component_type: Component type to filter by
            
        Returns:
            List of matching Component objects
        """
        params = {}
        if component_type:
            params["type"] = component_type.value
        
        try:
            response = self._client.get("/api/components", params=params)
            self._handle_response(response)
            return [Component(**item) for item in response.json()]
        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to {self.base_url}: {e}")
