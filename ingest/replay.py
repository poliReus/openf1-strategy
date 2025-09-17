import time
from ingest.openf1_client import fetch_laps, normalize_laps
from ingest.producer import make_producer, publish_record, flush

SESSION_KEY = 9159  # example: pick one from OpenF1 docs
TOPIC = "telemetry.raw"


def main():
    producer = make_producer()
    last_sent_lap = 0
    while True:
        laps = fetch_laps(SESSION_KEY, after_lap=last_sent_lap)
        if not laps:
            break
        recs = normalize_laps(laps)
        for rec in recs:
            publish_record(producer, TOPIC, rec)
            print(f"Sent lap {rec['lap_number']} driver {rec['driver_number']}")
            last_sent_lap = rec["lap_number"]
            time.sleep(0.35)  # simulate live pacing
    flush(producer)


if __name__ == "__main__":
    main()
