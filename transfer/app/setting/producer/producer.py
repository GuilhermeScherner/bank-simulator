import asyncio
from aiokafka import AIOKafkaProducer
import os
from dotenv import load_dotenv

loop = asyncio.get_event_loop()

load_dotenv()

KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')

producer = AIOKafkaProducer(
    loop=loop, client_id="money-transfer.py", bootstrap_servers="localhost:9092"
)