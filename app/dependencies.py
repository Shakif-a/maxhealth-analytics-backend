from .database import get_db
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

async def get_database() -> AsyncIOMotorDatabase:
    return get_db()