import requests

OPENF1_BASE_URL = "https://api.openf1.org/v1"


def fetch_laps(
    session_key: int, driver_number: int | None = None, after_lap: int | None = None
):
    params = {"session_key": session_key}
    if driver_number:
        params["driver_number"] = driver_number
    if after_lap:
        params["lap_number>"] = after_lap

    r = requests.get(f"{OPENF1_BASE_URL}/laps", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


def normalize_laps(laps: list[dict]) -> list[dict]:
    records = []
    for lap in laps:
        rec = {
            "ts": lap.get("date_start"),
            "session_key": lap.get("session_key"),
            "driver_number": lap.get("driver_number"),
            "lap_number": lap.get("lap_number"),
            "s1": lap.get("duration_sector_1"),
            "s2": lap.get("duration_sector_2"),
            "s3": lap.get("duration_sector_3"),
            "lap_time": lap.get("lap_duration"),
            "i1_speed": lap.get("i1_speed"),
            "i2_speed": lap.get("i2_speed"),
            "st_speed": lap.get("st_speed"),
            "is_pit_out_lap": lap.get("is_pit_out_lap"),
        }
        records.append(rec)
    return records
