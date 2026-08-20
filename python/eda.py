import duckdb

con = duckdb.connect()
query = """
SELECT
    VendorID,
    payment_type,
    COUNT(*) AS zero_distance_trips,
    COUNT(*) FILTER (
        WHERE PULocationID = DOLocationID
    ) AS same_location,
    COUNT(*) FILTER (
        WHERE PULocationID <> DOLocationID
    ) AS different_location
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE trip_distance = 0
GROUP BY VendorID, payment_type
ORDER BY zero_distance_trips DESC;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT
    VendorID,
    payment_type,
    COUNT(*) AS trips,

    ROUND(MIN(trip_distance), 2) AS min_distance,

    ROUND(
        QUANTILE_CONT(trip_distance, 0.25),
        2
    ) AS p25_distance,

    ROUND(
        QUANTILE_CONT(trip_distance, 0.50),
        2
    ) AS median_distance,

    ROUND(
        QUANTILE_CONT(trip_distance, 0.75),
        2
    ) AS p75_distance,

    ROUND(
        QUANTILE_CONT(trip_distance, 0.99),
        2
    ) AS p99_distance,

    ROUND(MAX(trip_distance), 2) AS max_distance

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')

GROUP BY VendorID, payment_type

ORDER BY VendorID, payment_type;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

