import json
from confluent_kafka import Producer


def make_producer(bootstrap: str = "localhost:9092"):
    return Producer({"bootstrap.servers": bootstrap})


def publish_record(producer, topic: str, record: dict):
    producer.produce(
        topic,
        key=str(record.get("driver_number")),
        value=json.dumps(record).encode("utf-8"),
    )
    producer.poll(0)  # trigger delivery callbacks


def flush(producer):
    producer.flush()
