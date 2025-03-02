from fastapi import FastAPI
from router import get_db_connection, ApiBridgeRouter
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Dynamic CRUD Example")

# Configure database connection
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME", "mydb"),
    "user": os.getenv("DB_USER", "user"),
    "password": os.getenv("DB_PASS", "password"),
}

# Create database engine
engine = get_db_connection(**db_config)

# Create and include dynamic CRUD router
crud_router = DynamicCrudRouter(engine)
app.include_router(crud_router.get_router())

@app.get("/")
def read_root():
    return {"message": "Dynamic CRUD API ready"}

# Run with: uvicorn simple_app:app --reload