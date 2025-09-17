import json
from confluent_kafka import Producer
from engine.config import KAFKA_BOOTSTRAP, TOPIC_OUT


def make_producer():
    return Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})


def publish_options(producer, strategy_msg: dict):
    producer.produce(
        TOPIC_OUT,
        key=str(strategy_msg["driver_number"]),
        value=json.dumps(strategy_msg).encode("utf-8"),
    )
    producer.poll(0)


def flush(producer):
    producer.flush(5)
