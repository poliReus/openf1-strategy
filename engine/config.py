import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC_IN = os.getenv("TOPIC_IN", "telemetry.raw")  # or telemetry.normalized
TOPIC_OUT = os.getenv("TOPIC_OUT", "strategy.options")

# Heuristic params
PIT_LOSS = float(os.getenv("PIT_LOSS", "21.0"))
DEG = {
    "S": float(os.getenv("DEG_S", "0.08")),
    "M": float(os.getenv("DEG_M", "0.06")),
    "H": float(os.getenv("DEG_H", "0.04")),
}
STINT = {
    "S": int(os.getenv("STINT_S", "14")),
    "M": int(os.getenv("STINT_M", "22")),
    "H": int(os.getenv("STINT_H", "30")),
}
