from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.joke_db

def get_db():
    return db

cognito_client = AsyncIOMotorClient(MONGODB_URL)
cognito_db = cognito_client.cognito

def get_cognito_db():
    return cognito_db