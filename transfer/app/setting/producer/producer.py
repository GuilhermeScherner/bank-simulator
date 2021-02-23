import asyncio
from aiokafka import AIOKafkaProducer
import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')

