# AeroSDK - Aerospace Data Processing Platform

A Python SDK + FastAPI backend for parsing, transforming, and managing aerospace engineering data.

## Features

- **Client SDK**: Type-safe Python library for aerospace data operations
- **FastAPI Backend**: REST API for file processing and data management
- **Data Layer**: PostgreSQL with ORM for aerospace structures
- **Docker Support**: Containerized deployment ready

## Tech Stack

- Python 3.11+
- FastAPI + Uvicorn
- SQLAlchemy + Alembic
- Pydantic for data validation
- PostgreSQL
- Docker

## Project Structure

```
aerosdk/
├── sdk/                    # Python SDK package
│   ├── __init__.py
│   ├── client.py          # Main SDK client
│   ├── models.py          # Pydantic models
│   └── exceptions.py      # Custom exceptions
├── server/                # FastAPI backend
│   ├── main.py           # Application entry point
│   ├── models.py         # Database models
│   ├── routes/           # API endpoints
│   └── database.py       # Database configuration
├── tests/                # Test suite
├── docker-compose.yml    # Local dev environment
├── Dockerfile            # Container definition
├── pyproject.toml        # Project metadata
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- UV (package manager)

### Setup

1. Clone and navigate to project:
```bash
cd aerosdk
```

2. Install dependencies:
```bash
uv sync
```

3. Start development environment:
```bash
docker-compose up
```

4. Run server:
```bash
uv run python server/main.py
```

## API Overview

- `POST /api/components/upload` - Upload aerospace component file
- `GET /api/components/{id}` - Retrieve component data
- `GET /api/components` - List all components

## SDK Usage

```python
from aerosdk.client import AeroClient

client = AeroClient("http://localhost:8000")
components = client.get_components()
```

## Development

Run tests:
```bash
uv run pytest
```

Format code:
```bash
uv run ruff format .
```

Lint:
```bash
uv run ruff check . --fix
```
