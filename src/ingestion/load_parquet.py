import sys

import duckdb
import psycopg2
from psycopg2.extras import execute_values

from config import PG_CONFIG


# ---------------------------------------------------------
# Dataset configuration
# ---------------------------------------------------------

DATASETS = {
    "yellow": {
        "file": "../../data/raw/yellow_tripdata_2026-01.parquet",
        "table": "staging.yellow_trips",
    },
    "green": {
        "file": "../../data/raw/green_tripdata_2026-01.parquet",
        "table": "staging.green_trips",
    },
    "fhv": {
        "file": "../../data/raw/fhv_tripdata_2026-01.parquet",
        "table": "staging.fhv_trips",
    },
    "fhvhv": {
        "file": "../../data/raw/fhvhv_tripdata_2026-01.parquet",
        "table": "staging.fhvhv_trips",
    },
}


# ---------------------------------------------------------
# Get dataset from command line
# ---------------------------------------------------------

if len(sys.argv) != 2:
    print("Usage: python load_parquet.py <dataset>")
    print("Available datasets: yellow, green, fhv, fhvhv")
    sys.exit(1)


dataset_name = sys.argv[1].lower()

if dataset_name not in DATASETS:
    print(f"Unknown dataset: {dataset_name}")
    print("Available datasets: yellow, green, fhv, fhvhv")
    sys.exit(1)


dataset = DATASETS[dataset_name]

PARQUET_FILE = dataset["file"]
TARGET_TABLE = dataset["table"]


# ---------------------------------------------------------
# Read Parquet with DuckDB
# ---------------------------------------------------------

duck = duckdb.connect()

query = f"""
SELECT *
FROM read_parquet('{PARQUET_FILE}')
"""

result = duck.execute(query)

columns = [column[0] for column in result.description]

print(f"Dataset: {dataset_name}")
print(f"Columns: {len(columns)}")


# ---------------------------------------------------------
# Connect to PostgreSQL
# ---------------------------------------------------------

conn = psycopg2.connect(**PG_CONFIG)
cursor = conn.cursor()


# ---------------------------------------------------------
# Insert data in batches
# ---------------------------------------------------------

batch_size = 10_000
total_rows = 0

placeholders = ", ".join(["%s"] * len(columns))

insert_query = f"""
INSERT INTO {TARGET_TABLE}
VALUES ({placeholders})
"""


while True:

    rows = result.fetchmany(batch_size)

    if not rows:
        break

    cursor.executemany(insert_query, rows)

    total_rows += len(rows)

    print(f"Inserted: {total_rows:,} rows")


# ---------------------------------------------------------
# Commit
# ---------------------------------------------------------

conn.commit()

print()
print(f"Total rows inserted: {total_rows:,}")
print("Ingestion complete.")


# ---------------------------------------------------------
# Close connections
# ---------------------------------------------------------

cursor.close()
conn.close()
duck.close()