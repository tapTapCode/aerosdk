"""
Tests for the AeroSDK client.
"""

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from sdk.client import AeroClient
from sdk.models import Component, ComponentCreate, ComponentType
from sdk.exceptions import ConnectionError, NotFoundError


@pytest.fixture
def client():
    """Create a test client."""
    return AeroClient("http://localhost:8000")


@pytest.fixture
def sample_component():
    """Create a sample component."""
    return Component(
        id=1,
        name="Wing Assembly",
        description="Main wing",
        component_type=ComponentType.WING,
        weight_kg=450.0,
        material="Aluminum",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def test_client_initialization(client):
    """Test client initialization."""
    assert client.base_url == "http://localhost:8000"
    assert client.timeout == 10.0


def test_client_context_manager():
    """Test client context manager."""
    with AeroClient("http://localhost:8000") as client:
        assert client.base_url == "http://localhost:8000"


def test_get_components_success(client, sample_component):
    """Test successful get components."""
    with patch.object(client._client, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [sample_component.model_dump()]
        mock_get.return_value = mock_response
        
        components = client.get_components()
        
        assert len(components) == 1
        assert components[0].id == 1
        assert components[0].name == "Wing Assembly"


def test_get_component_success(client, sample_component):
    """Test successful get single component."""
    with patch.object(client._client, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_component.model_dump()
        mock_get.return_value = mock_response
        
        component = client.get_component(1)
        
        assert component.id == 1
        assert component.name == "Wing Assembly"


def test_get_component_not_found(client):
    """Test get component not found."""
    with patch.object(client._client, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        mock_get.return_value = mock_response
        
        with pytest.raises(NotFoundError):
            client.get_component(999)


def test_create_component_success(client, sample_component):
    """Test successful component creation."""
    with patch.object(client._client, "post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = sample_component.model_dump()
        mock_post.return_value = mock_response
        
        component_data = ComponentCreate(
            name="Wing Assembly",
            description="Main wing",
            component_type=ComponentType.WING,
            weight_kg=450.0,
            material="Aluminum",
        )
        
        created = client.create_component(component_data)
        
        assert created.id == 1
        assert created.name == "Wing Assembly"


def test_delete_component_success(client):
    """Test successful component deletion."""
    with patch.object(client._client, "delete") as mock_delete:
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response
        
        client.delete_component(1)
        
        mock_delete.assert_called_once_with("/api/components/1")


def test_filter_components_by_type(client, sample_component):
    """Test filtering components by type."""
    with patch.object(client._client, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [sample_component.model_dump()]
        mock_get.return_value = mock_response
        
        components = client.filter_components(component_type=ComponentType.WING)
        
        assert len(components) == 1
        assert components[0].component_type == ComponentType.WING


def test_connection_error(client):
    """Test connection error handling."""
    import httpx
    
    with patch.object(client._client, "get") as mock_get:
        mock_get.side_effect = httpx.ConnectError("Connection failed")
        
        with pytest.raises(ConnectionError):
            client.get_components()
