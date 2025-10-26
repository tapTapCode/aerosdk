# AeroSDK Learning Guide

This document explains the key concepts and architecture patterns used in this project. Understanding these will help you in interviews and with Python development.

## Architecture Overview

```
Client SDK (sdk/)          Backend Server (server/)      Database
─────────────────────      ─────────────────────────     ────────
┌──────────────────┐       ┌──────────────────────┐       PostgreSQL
│  AeroClient      │──────▶│  FastAPI App         │◀─────▶│
│  (makes HTTP     │       │  (handles requests)  │       │
│   requests)      │       │                      │       │
└──────────────────┘       └──────────────────────┘       │
                                    │                      │
                                    ├─ Models (SQLAlchemy)──
                                    ├─ Routes (CRUD logic)
                                    └─ Database config
```

## Key Concepts Explained

### 1. **Pydantic Models** (sdk/models.py & server/models.py)

**What:** Data validation and serialization layer.

**Why:** Ensures data integrity - Pydantic validates incoming data against defined schemas.

**Example:**
```python
# This automatically validates that weight_kg > 0
class ComponentBase(BaseModel):
    weight_kg: float = Field(..., gt=0)
```

**Interview tip:** Pydantic is heavily used in FastAPI. Understand `BaseModel`, field validation, and the difference between `model_dump()` and serialization.

### 2. **SQLAlchemy Models** (server/models.py)

**What:** Object-Relational Mapping (ORM) - maps Python classes to database tables.

**Why:** You write Python code instead of SQL queries. SQLAlchemy handles the translation.

**Example:**
```python
# Python
component = db.query(ComponentModel).filter(ComponentModel.id == 1).first()

# Translates to SQL:
# SELECT * FROM components WHERE id = 1 LIMIT 1;
```

**Interview tip:** Explain what an ORM is - it abstracts database operations into Python objects.

### 3. **FastAPI Routes** (server/routes.py)

**What:** REST API endpoints that handle HTTP requests.

**Why:** Different endpoints for different operations (GET all, GET one, POST create, PUT update, DELETE).

**REST Pattern (CRUD):**
- `GET /api/components` - **Read** all components
- `GET /api/components/{id}` - **Read** one component
- `POST /api/components` - **Create** a component
- `PUT /api/components/{id}` - **Update** a component
- `DELETE /api/components/{id}` - **Delete** a component

**Interview tip:** Know HTTP methods: GET (retrieve), POST (create), PUT (update), DELETE (remove).

### 4. **Dependency Injection** (server/routes.py)

**What:** FastAPI's `Depends` mechanism automatically provides dependencies.

```python
# The db session is automatically provided to every route
@router.get("")
def list_components(db: Session = Depends(get_db)):
    return db.query(ComponentModel).all()
```

**Why:** Clean, testable code. Easy to mock dependencies in tests.

**Interview tip:** Understand why dependency injection is better than global variables.

### 5. **Client SDK** (sdk/client.py)

**What:** A Python library users import to interact with the backend.

**Why:** Abstracts HTTP details from users. Provides nice Python methods.

**Usage:**
```python
from aerosdk import AeroClient

client = AeroClient("http://localhost:8000")
components = client.get_components()
```

**Interview tip:** This is what distinguishes this from just a "backend API" - you're building both the library AND the backend.

### 6. **Exception Handling** (sdk/exceptions.py)

**What:** Custom exceptions for specific error scenarios.

**Why:** Allows clients to catch specific errors and handle them appropriately.

```python
try:
    component = client.get_component(999)
except NotFoundError:
    print("Component doesn't exist")
except ConnectionError:
    print("Backend is unavailable")
```

**Interview tip:** Always create domain-specific exceptions, not generic ones.

## Database Layer Explained

### Connection Flow:

1. **database.py** creates the database engine and session factory
2. **Routes** request a session via `Depends(get_db)`
3. **SQLAlchemy** handles queries and translations
4. **PostgreSQL** executes the actual SQL

### Why PostgreSQL?

- Relational data (components belong to assemblies)
- ACID compliance (transactions are reliable)
- Proper enum types support
- Production-ready

## Testing Strategy

**File:** tests/test_client.py

**Key Pattern:** Mock the HTTP responses

```python
with patch.object(client._client, "get") as mock_get:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [...]
    mock_get.return_value = mock_response
    
    result = client.get_components()
```

**Why:** You test the client logic without needing the real server running.

## Important Python Patterns Used

### 1. Context Managers (`__enter__`, `__exit__`)

```python
# Automatic cleanup
with AeroClient("http://localhost:8000") as client:
    components = client.get_components()
# Client is closed automatically
```

### 2. Type Hints

```python
def get_components(self) -> List[Component]:
    """Return type is List of Component objects"""
```

**Why:** Helps catch bugs, enables IDE autocompletion, documents code.

### 3. Enums

```python
class ComponentType(str, Enum):
    WING = "wing"
    ENGINE = "engine"
```

**Why:** Type-safe constants. Can't accidentally pass invalid component type.

### 4. List Comprehensions

```python
# Convert list of dicts to Component objects
return [Component(**item) for item in response.json()]
```

### 5. Docstrings (PEP 257)

```python
def create_component(self, component: ComponentCreate) -> Component:
    """
    Create a new component.
    
    Args:
        component: ComponentCreate object with component data
    
    Returns:
        Created Component object
    
    Raises:
        ValidationError: If data validation fails
    """
```

**Why:** Professional code has documentation. Helps with API understanding.

## Next Steps to Learn

1. **Run the project** - See it working
2. **Add file parsing** - Parse aerospace files (STEP, IGES)
3. **Add database migrations** - Use Alembic
4. **Add authentication** - JWT tokens
5. **Add async/await** - FastAPI async routes for better performance
6. **Deploy to AWS** - EC2, RDS, S3

## Interview Questions You Should Be Able to Answer

1. "What's the difference between Pydantic models and SQLAlchemy models?"
   - **Answer:** Pydantic validates/serializes data. SQLAlchemy maps to database tables.

2. "Why use dependency injection?"
   - **Answer:** Makes code testable, reusable, and decoupled.

3. "How would you handle pagination for large datasets?"
   - **Answer:** Add `skip` and `limit` parameters to queries.

4. "What's the difference between POST and PUT?"
   - **Answer:** POST creates new resource. PUT updates existing resource.

5. "How do you ensure database consistency?"
   - **Answer:** ACID transactions, proper indexing, constraints.

## Running & Testing

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Format code
uv run ruff format .

# Lint code
uv run ruff check . --fix

# Type check
uv run mypy .

# Run server (with Docker)
docker-compose up
```

Good luck! This is solid material for an interview.
