import json
import threading
from confluent_kafka import Consumer
from api.config import KAFKA_BOOTSTRAP, TOPIC_STRATEGY
from api.models import StrategyResponse
from api.state import update_driver_options


def make_consumer():
    return Consumer(
        {
            "bootstrap.servers": KAFKA_BOOTSTRAP,
            "group.id": "api-consumer-1",
            "auto.offset.reset": "latest",
        }
    )


def consume_forever():
    consumer = make_consumer()
    consumer.subscribe([TOPIC_STRATEGY])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error:", msg.error())
                continue

            rec = json.loads(msg.value().decode("utf-8"))
            try:
                parsed = StrategyResponse(**rec)
                update_driver_options(parsed.driver_number, parsed)
            except Exception as e:
                print("Failed to parse strategy option:", e)

    except KeyboardInterrupt:
        print("Stopping API consumer...")
    finally:
        consumer.close()


def start_consumer_thread():
    thread = threading.Thread(target=consume_forever, daemon=True)
    thread.start()
