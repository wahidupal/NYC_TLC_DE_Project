import duckdb

con = duckdb.connect()
query = """
SELECT
    payment_type,
    MIN(trip_distance) AS min_distance,
    MAX(trip_distance) AS max_distance,
    MIN(total_amount) AS min_total,
    MAX(total_amount) AS max_total
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
GROUP BY payment_type
ORDER BY payment_type;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT
    trip_distance,
    total_amount,
    total_amount / NULLIF(trip_distance, 0) AS dollars_per_mile
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE payment_type = 0
  AND trip_distance > 0
ORDER BY dollars_per_mile DESC
LIMIT 20;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()
