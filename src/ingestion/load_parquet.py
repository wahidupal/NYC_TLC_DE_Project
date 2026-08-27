import duckdb
import psycopg2


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

PARQUET_FILE = "../../data/raw/yellow_tripdata_2026-01.parquet"

PG_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "nyc_tlc",
    "user": "postgres",
    "password": "W@hman140890"
}


# ---------------------------------------------------------
# Connect to PostgreSQL
# ---------------------------------------------------------

conn = psycopg2.connect(**PG_CONFIG)
cursor = conn.cursor()


# ---------------------------------------------------------
# Read Parquet with DuckDB
# ---------------------------------------------------------

duck = duckdb.connect()

query = f"""
SELECT *
FROM read_parquet('{PARQUET_FILE}')
"""

rows = duck.execute(query).fetchall()

print(f"Rows read from Parquet: {len(rows):,}")


# ---------------------------------------------------------
# Insert into PostgreSQL
# ---------------------------------------------------------

insert_query = """
INSERT INTO staging.yellow_trips (
    vendorid,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    passenger_count,
    trip_distance,
    ratecodeid,
    store_and_fwd_flag,
    pulocationid,
    dolocationid,
    payment_type,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    airport_fee,
    cbd_congestion_fee
)
VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s
)
"""

cursor.executemany(insert_query, rows)

conn.commit()

print(f"Rows inserted into PostgreSQL: {cursor.rowcount:,}")


# ---------------------------------------------------------
# Close connections
# ---------------------------------------------------------

cursor.close()
conn.close()
duck.close()

print("Ingestion complete.")