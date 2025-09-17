import json
import os
from collections import defaultdict
from datetime import datetime
from confluent_kafka import Consumer
from engine.config import KAFKA_BOOTSTRAP, TOPIC_IN
from engine.model import score_options
from engine.producer import make_producer, publish_options, flush

TOTAL_LAPS_DEFAULT = int(
    os.getenv("TOTAL_LAPS_DEFAULT", "60")
)  # override per session if you know


def make_consumer():
    return Consumer(
        {
            "bootstrap.servers": KAFKA_BOOTSTRAP,
            "group.id": "engine-consumer-1",
            "auto.offset.reset": "earliest",
        }
    )


def run_engine():
    consumer = make_consumer()
    producer = make_producer()
    consumer.subscribe([TOPIC_IN])

    # driver state: per driver track last lap & laps_times
    # state[driver] = {"last_lap": int, "laps_times": [float,...], "compound": "M"}
    state = defaultdict(lambda: {"last_lap": 0, "laps_times": [], "compound": "M"})
    session_key_seen = None

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error:", msg.error())
                continue

            rec = json.loads(msg.value().decode("utf-8"))
            # Expect Phase 1 shape: ts, session_key, driver_number, lap_number, lap_time, ...
            session_key = rec.get("session_key")
            session_key_seen = session_key or session_key_seen
            driver = rec.get("driver_number")
            lap = rec.get("lap_number")
            lap_time = rec.get("lap_time")

            if driver is None or lap is None:
                continue

            st = state[driver]
            st["last_lap"] = max(st["last_lap"], int(lap))
            # append lap time if numeric
            if isinstance(lap_time, (int, float)) and lap_time > 0:
                st["laps_times"].append(float(lap_time))

            # compute options each lap
            options = score_options(st, TOTAL_LAPS_DEFAULT)
            out = {
                "timestamp": datetime.utcnow().isoformat(),
                "session_key": session_key_seen,
                "driver_number": driver,
                "lap": st["last_lap"],
                "options": options,
            }
            publish_options(producer, out)

    except KeyboardInterrupt:
        print("Stopping engine...")
    finally:
        flush(producer)
        consumer.close()
