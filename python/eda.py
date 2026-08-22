import duckdb

con = duckdb.connect()
query = """
SELECT
    VendorID,
    payment_type,
    trip_distance,
    fare_amount,
    total_amount,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    PULocationID,
    DOLocationID
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE VendorID = 7
  AND tpep_dropoff_datetime = tpep_pickup_datetime
LIMIT 20;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT
    COUNT(*) AS total_trips,
    COUNT(*) FILTER (
        WHERE tpep_dropoff_datetime = tpep_pickup_datetime
    ) AS zero_duration_trips,
    COUNT(*) FILTER (
        WHERE tpep_dropoff_datetime > tpep_pickup_datetime
    ) AS positive_duration_trips,
    COUNT(*) FILTER (
        WHERE tpep_dropoff_datetime < tpep_pickup_datetime
    ) AS negative_duration_trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE VendorID = 7;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT
    MIN(tpep_pickup_datetime) AS first_pickup,
    MAX(tpep_pickup_datetime) AS last_pickup,
    COUNT(DISTINCT CAST(tpep_pickup_datetime AS DATE)) AS active_days,
    COUNT(DISTINCT PULocationID) AS pickup_zones,
    COUNT(DISTINCT DOLocationID) AS dropoff_zones
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE VendorID = 7;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

