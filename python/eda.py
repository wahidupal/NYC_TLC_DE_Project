import duckdb

con = duckdb.connect()
query = """
SELECT
    COUNT(*) AS total_trips,
    COUNT(*) FILTER (WHERE trip_distance > 20) AS over_20,
    COUNT(*) FILTER (WHERE trip_distance > 50) AS over_50,
    COUNT(*) FILTER (WHERE trip_distance > 100) AS over_100,
    COUNT(*) FILTER (WHERE trip_distance > 20 AND trip_distance < 100) AS between_20_100,
    COUNT(*) FILTER (WHERE trip_distance > 500) AS over_500,
    COUNT(*) FILTER (WHERE trip_distance > 1000) AS over_1k,
    COUNT(*) FILTER (WHERE trip_distance > 10000) AS over_10k,
    COUNT(*) FILTER (WHERE trip_distance > 100000) AS over_100k

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE VendorID = 2;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT
    COUNT(*) AS total_trips,
    COUNT(*) FILTER (WHERE trip_distance > 20) AS over_20,
    COUNT(*) FILTER (WHERE trip_distance > 50) AS over_50,
    COUNT(*) FILTER (WHERE trip_distance > 100) AS over_100,
    COUNT(*) FILTER (WHERE trip_distance > 20 AND trip_distance < 100) AS between_20_100,
    COUNT(*) FILTER (WHERE trip_distance > 500) AS over_500,
    COUNT(*) FILTER (WHERE trip_distance > 1000) AS over_1k,
    COUNT(*) FILTER (WHERE trip_distance > 10000) AS over_10k,
    COUNT(*) FILTER (WHERE trip_distance > 100000) AS over_100k

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT
    payment_type,
    RatecodeID,
    COUNT(*) AS trips,
    MIN(trip_distance) AS min_distance,
    MAX(trip_distance) AS max_distance
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE VendorID = 2
  AND trip_distance > 500
GROUP BY payment_type, RatecodeID
ORDER BY trips DESC;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

