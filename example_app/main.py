from fastapi import FastAPI
from api.v2 import v2_base


app = FastAPI(root_path="/api-bridge")

app.include_router(v2_base.router, prefix="/v1", tags=["API V1 Bridge"])
