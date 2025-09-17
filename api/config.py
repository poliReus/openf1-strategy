import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC_STRATEGY = os.getenv("TOPIC_STRATEGY", "strategy.options")
API_PORT = int(os.getenv("API_PORT", "8000"))
