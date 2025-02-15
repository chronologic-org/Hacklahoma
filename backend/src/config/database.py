from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "hacklahoma")

class Database:
    client: AsyncIOMotorClient = None
    
async def connect_to_mongo():
    Database.client = AsyncIOMotorClient(
        MONGODB_URL,
        server_api=ServerApi('1')
    )
    try:
        # Verify the connection
        await Database.client.admin.command('ping')
        print("✅ Connected to MongoDB!")
    except Exception as e:
        print(f"❌ Could not connect to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    if Database.client:
        Database.client.close()
        print("Closed MongoDB connection") 