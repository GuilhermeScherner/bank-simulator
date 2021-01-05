from fastapi import FastAPI
from odmantic import AIOEngine
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
import os
from odmantic import Field, Model
from dotenv import load_dotenv
import asyncio
from aiokafka import AIOKafkaConsumer

app = FastAPI()

client = AsyncIOMotorClient("mongodb://admin:admin@localhost:27017/")

engine = AIOEngine(motor_client=client, database="example_db")

load_dotenv()

KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')


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


async def consume(consumer):
    try:
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        await consumer.stop()


@app.on_event("startup")
async def startup_event() -> None:
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, client_id="money-transfer", bootstrap_servers="localhost:9092")
    app.state.consumer = consumer
    await app.state.consumer.start()
    asyncio.ensure_future(consume(app.state.consumer))