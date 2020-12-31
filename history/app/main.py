from fastapi import FastAPI
from odmantic import AIOEngine
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient

from odmantic import Field, Model
app = FastAPI()

client = AsyncIOMotorClient("mongodb://admin:admin@localhost:27017/")

engine = AIOEngine(motor_client=client, database="example_db")


class Publisher(Model):
    name: str
    founded: int = Field(ge=1440)
    location: Optional[str] = None


instances = [
    Publisher(name="HarperCollins", founded=1989, location="US"),
    Publisher(name="Hachette Livre", founded=1826, location="FR"),
    Publisher(name="Lulu", founded=2002)
]


@app.get("/")
async def test():
    result = await engine.save_all(instances)
    early_publishers = await engine.find(Publisher)
    print(early_publishers)
    return {"maslkd": "Joknoand"}
