from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

client = AsyncIOMotorClient("mongodb://admin:admin@localhost:27017/")

engine = AIOEngine(motor_client=client, database="history")