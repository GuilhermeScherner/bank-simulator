from fastapi import APIRouter, Depends, HTTPException, FastAPI
from app.setting.consumer.consumer import engine, KAFKA_TOPIC
from aiokafka import AIOKafkaConsumer
import asyncio
from app.application.models.history import History


app = FastAPI()

@app.get("")
async def get_all_transfer():
    early_publishers = await engine.find(History)
    return early_publishers


async def consume(consumer):
    try:
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
            await engine.save_all(msg)
    finally:
        await consumer.stop()


@app.on_event("startup")
async def startup_event() -> None:
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, client_id="money-transfer", bootstrap_servers="localhost:9092")
    app.state.consumer = consumer
    await app.state.consumer.start()
    asyncio.ensure_future(consume(app.state.consumer))
