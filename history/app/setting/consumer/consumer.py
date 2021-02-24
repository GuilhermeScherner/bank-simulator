from dotenv import load_dotenv
import os



load_dotenv()

KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
