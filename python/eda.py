import duckdb

con = duckdb.connect()
query = """
SELECT
    payment_type,
    COUNT(*) AS trips,
    ROUND(AVG(trip_distance), 2) AS avg_distance,
    ROUND(AVG(total_amount), 2) AS avg_total_amount,
    ROUND(AVG(total_amount / NULLIF(trip_distance, 0)), 2) AS avg_dollars_per_mile
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
    payment_type,
    COUNT(*) AS trips,

    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(SUM(trip_distance), 2) AS total_miles,

    ROUND(
        SUM(total_amount) / NULLIF(SUM(trip_distance), 0),
        2
    ) AS revenue_per_mile

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
    payment_type,
    ROUND(AVG(fare_amount), 2) AS avg_fare,
    ROUND(AVG(total_amount), 2) AS avg_total,
    ROUND(AVG(total_amount - fare_amount), 2) AS avg_difference
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
GROUP BY payment_type
ORDER BY payment_type;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()