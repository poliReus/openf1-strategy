import pandas as pd

df = pd.read_parquet(
    "../parquet_output/session_key=9159/driver_number=1/0ae7afffa7a742ef98eae9d782d13d31-0.parquet"
)
print(df.dtypes)  # check inferred dtypes
print(df.head())  # preview first rows
