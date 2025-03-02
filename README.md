# api-bridge

A flexible, dynamic CRUD (Create, Read, Update, Delete) operations library for FastAPI applications with MySQL database support.

## Features

- Dynamic CRUD operations for any MySQL table
- Simple integration with FastAPI
- Automatic pagination
- Support for hard delete and soft delete operations
- Support for partial updates via PATCH method
- Configurable database connection

## Installation

```bash
pip install api-bridge
```

## Quick Start

```python
from fastapi import FastAPI
from dynamic_crud import get_db_connection, DynamicCrudRouter

app = FastAPI()

# Configure database connection
db_config = {
    "host": "localhost",
    "port": 3306,
    "database": "mydb",
    "user": "username",
    "password": "password@123",
}

# Create database engine
engine = get_db_connection(**db_config)

# Create and include dynamic CRUD router
crud_router = DynamicCrudRouter(engine)
app.include_router(crud_router.get_router())

# Run with uvicorn
# uvicorn main:app --reload
```

## API Routes

| Method | Route                        | Description                     |
|--------|------------------------------|---------------------------------|
| GET    | /base/test                   | Test database connection        |
| GET    | /base/{table_name}           | List records with pagination    |
| POST   | /base/{table_name}           | Create a new record             |
| PUT    | /base/{table_name}/{id}      | Update a record completely      |
| PATCH  | /base/{table_name}/{id}      | Update specific fields          |
| DELETE | /base/{table_name}/{id}      | Soft delete a record            |
| DELETE | /base/{table_name}/{id}/hard | Hard delete a record            |

## Example Applications

### 1. E-commerce Product Management System

Manage products, categories, inventory, and orders using dynamic CRUD operations:

```python
from fastapi import FastAPI
from dynamic_crud import get_db_connection, DynamicCrudRouter
import os

app = FastAPI(title="E-commerce API")

# Load database config
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME", "ecommerce"),
    "user": os.getenv("DB_USER", "user"),
    "password": os.getenv("DB_PASS", "password"),
}

# Connect to database
engine = get_db_connection(**db_config)

# Create dynamic routers
crud_router = DynamicCrudRouter(engine)
app.include_router(crud_router.get_router())

# Add custom routes as needed
@app.get("/")
def read_root():
    return {"message": "E-commerce API ready"}
```

Database tables like `products`, `categories`, `inventory`, and `orders` are automatically available through the dynamic CRUD routes.

### 2. Content Management System (CMS)

Manage blog posts, pages, users, and media files:

```python
from fastapi import FastAPI
from dynamic_crud import get_db_connection, DynamicCrudRouter
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="CMS API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load database config
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME", "cms"),
    "user": os.getenv("DB_USER", "user"),
    "password": os.getenv("DB_PASS", "password"),
}

# Connect to database
engine = get_db_connection(**db_config)

# Create dynamic router
crud_router = DynamicCrudRouter(engine, prefix="/api")
app.include_router(crud_router.get_router())

# Add custom routes
@app.get("/")
def read_root():
    return {"message": "CMS API ready"}
```

Database tables like `posts`, `pages`, `users`, and `media` are automatically available through the dynamic CRUD routes.

## Workflow to Publish as a PIP Module

1. **Prepare Your Package Structure**:
   ```
   dynamic-crud-fastapi/
   ├── dynamic_crud/
   │   ├── __init__.py
   │   ├── db.py
   │   └── router.py
   ├── setup.py
   ├── README.md
   ├── LICENSE
   └── requirements.txt
   ```

2. **Test Your Package Locally**:
   ```bash
   pip install -e .
   ```

3. **Build Your Package**:
   ```bash
   pip install build
   python -m build
   ```

4. **Upload to PyPI Test**:
   ```bash
   pip install twine
   twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   ```

5. **Test Your Package from TestPyPI**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ dynamic-crud-fastapi
   ```

6. **Upload to PyPI**:
   ```bash
   twine upload dist/*
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.