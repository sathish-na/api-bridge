from fastapi import FastAPI
from api_bridge import APIBridge

# Single database configuration
db_config = {
    "host": "localhost",
    "port": 3306,
    "database": "mydb",
    "user": "root",
    "password": "password"
}

app = FastAPI()
api_bridge = APIBridge(db_config)
app.include_router(api_bridge.router)

# Run the app
# uvicorn main:app --reload
