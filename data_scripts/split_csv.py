import math

import pandas as pd

calendar_df = pd.read_csv("datasets/calendar.csv/calendar.csv")
listings_df = pd.read_csv("datasets/listings-2.csv/listings-2.csv")

MAX_SIZE = 25 * 1024 * 1024  # 25 MB

def split_dataframe(df, max_size, base_filename, safety=0.95):
    # Measure the real CSV size on a sample to estimate bytes/row
    sample = df.head(min(len(df), 10_000))
    sample_bytes = len(sample.to_csv(index=False).encode("utf-8"))
    bytes_per_row = sample_bytes / len(sample)

    rows_per_file = max(1, int(max_size * safety / bytes_per_row))
    n_files = math.ceil(len(df) / rows_per_file)

    for i in range(n_files):
        chunk = df.iloc[i * rows_per_file : (i + 1) * rows_per_file]
        chunk.to_csv(f"{base_filename}_{i + 1}.csv", index=False)

split_dataframe(calendar_df, MAX_SIZE, "calendar_split")
split_dataframe(listings_df, MAX_SIZE, "listings_split")
