import json
import os
import pyarrow as pa
import pyarrow.parquet as pq
from confluent_kafka import Consumer

# -------------------------------------------------------------------
# Config
# -------------------------------------------------------------------
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "telemetry.raw")
PARQUET_DIR = os.getenv("PARQUET_DIR", "parquet_output")


# -------------------------------------------------------------------
# Safe casting helpers
# -------------------------------------------------------------------
def safe_int(value):
    try:
        if value is None or value == "":
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def safe_float(value):
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def safe_bool(value):
    if value in [True, "True", "true", 1, "1"]:
        return True
    if value in [False, "False", "false", 0, "0"]:
        return False
    return None


# -------------------------------------------------------------------
# Kafka Consumer
# -------------------------------------------------------------------
def make_consumer():
    return Consumer(
        {
            "bootstrap.servers": KAFKA_BOOTSTRAP,
            "group.id": "normalize-consumer-1",  # change id to reset offsets
            "auto.offset.reset": "earliest",
        }
    )


def consume_and_store(batch_size: int = 1):
    consumer = make_consumer()
    consumer.subscribe([TOPIC])

    buffer = []

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error:", msg.error())
                continue

            record = json.loads(msg.value().decode("utf-8"))
            buffer.append(record)

            if len(buffer) >= batch_size:
                flush_buffer(buffer)
                buffer = []

    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        if buffer:
            flush_buffer(buffer)
        consumer.close()


# -------------------------------------------------------------------
# Flush buffer to Parquet
# -------------------------------------------------------------------
def flush_buffer(records: list[dict]):
    if not records:
        return

    casted = []
    for r in records:
        casted.append(
            {
                "ts": r.get("ts"),
                "session_key": safe_int(r.get("session_key")),
                "driver_number": safe_int(r.get("driver_number")),
                "lap_number": safe_int(r.get("lap_number")),
                "s1": safe_float(r.get("s1")),
                "s2": safe_float(r.get("s2")),
                "s3": safe_float(r.get("s3")),
                "lap_time": safe_float(r.get("lap_time")),
                "i1_speed": safe_int(r.get("i1_speed")),
                "i2_speed": safe_int(r.get("i2_speed")),
                "st_speed": safe_int(r.get("st_speed")),
                "is_pit_out_lap": safe_bool(r.get("is_pit_out_lap")),
            }
        )

    # Let Arrow infer schema instead of enforcing laps_schema
    table = pa.Table.from_pylist(casted)

    os.makedirs(PARQUET_DIR, exist_ok=True)
    pq.write_to_dataset(
        table, root_path=PARQUET_DIR, partition_cols=["session_key", "driver_number"]
    )
    print(f"Flushed {len(records)} records to {PARQUET_DIR}")


# -------------------------------------------------------------------
# Entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    consume_and_store(batch_size=1)
