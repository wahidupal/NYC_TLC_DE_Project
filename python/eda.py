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
    tpep_dropoff_datetime
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE trip_distance > 1000
ORDER BY trip_distance DESC
LIMIT 20;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT
    payment_type,
    COUNT(*) AS negative_trips,
    ROUND(SUM(total_amount), 2) AS negative_total
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE total_amount < 0
GROUP BY payment_type
ORDER BY negative_trips DESC;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT
    payment_type,
    COUNT(*) AS zero_distance_trips,
    ROUND(AVG(total_amount), 2) AS avg_total,
    ROUND(AVG(fare_amount), 2) AS avg_fare
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE trip_distance = 0
GROUP BY payment_type
ORDER BY zero_distance_trips DESC;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()
