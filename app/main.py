from fastapi import FastAPI
from .routers import jokes
from .database import client

app = FastAPI()

# Include routers
app.include_router(jokes.router, prefix="/jokes", tags=["jokes"])

@app.on_event("shutdown")
async def shutdown_event():
    client.close()