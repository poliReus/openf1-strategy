import pyarrow as pa

laps_schema = pa.schema(
    [
        ("ts", pa.timestamp("ms")),  # start time of the lap
        ("session_key", pa.int32()),
        ("driver_number", pa.int32()),
        ("lap_number", pa.int32()),
        ("s1", pa.float32()),
        ("s2", pa.float32()),
        ("s3", pa.float32()),
        ("lap_time", pa.float32()),
        ("i1_speed", pa.int32()),
        ("i2_speed", pa.int32()),
        ("st_speed", pa.int32()),
        ("is_pit_out_lap", pa.bool_()),
    ]
)
