import json
from confluent_kafka import Producer
import os


def make_producer(bootstrap: str = "localhost:9092"):
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
    return Producer({"bootstrap.servers": bootstrap_servers})


def publish_record(producer, topic: str, record: dict):
    producer.produce(
        topic,
        key=str(record.get("driver_number")),
        value=json.dumps(record).encode("utf-8"),
    )
    producer.poll(0)  # trigger delivery callbacks


def flush(producer):
    producer.flush()
