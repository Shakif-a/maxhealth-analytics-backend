from fastapi import FastAPI
from .routers import jokes, cognito
from .database import client

app = FastAPI()

# Include routers
app.include_router(jokes.router, prefix="/jokes", tags=["jokes"])
app.include_router(cognito.router, prefix="/cognito", tags=["cognito"])

@app.on_event("shutdown")
async def shutdown_event():
    client.close()