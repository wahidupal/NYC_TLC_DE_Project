import duckdb

con = duckdb.connect()
query = """
SELECT
    VendorID,
    payment_type,
    COUNT(*) AS trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE payment_type = 0
GROUP BY VendorID, payment_type
ORDER BY trips DESC;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT
    payment_type,
    COUNT(*) AS zero_distance_trips,

    ROUND(
        AVG(
            EXTRACT(EPOCH FROM (
                tpep_dropoff_datetime - tpep_pickup_datetime
            )) / 60
        ),
        2
    ) AS avg_duration_minutes

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')

WHERE trip_distance = 0

GROUP BY payment_type
ORDER BY payment_type;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

