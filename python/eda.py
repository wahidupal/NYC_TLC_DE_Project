import duckdb

con = duckdb.connect()
query = """
SELECT
    VendorID,
    payment_type,
    COUNT(*) AS trips,

    ROUND(
        AVG(
            EXTRACT(EPOCH FROM (
                tpep_dropoff_datetime - tpep_pickup_datetime
            )) / 60
        ),
        2
    ) AS avg_duration_minutes,

    ROUND(
        QUANTILE_CONT(
            EXTRACT(EPOCH FROM (
                tpep_dropoff_datetime - tpep_pickup_datetime
            )) / 60,
            0.50
        ),
        2
    ) AS median_duration_minutes,

    ROUND(
        QUANTILE_CONT(
            EXTRACT(EPOCH FROM (
                tpep_dropoff_datetime - tpep_pickup_datetime
            )) / 60,
            0.99
        ),
        2
    ) AS p99_duration_minutes,

    ROUND(
        MAX(
            EXTRACT(EPOCH FROM (
                tpep_dropoff_datetime - tpep_pickup_datetime
            )) / 60
        ),
        2
    ) AS max_duration_minutes

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')

GROUP BY VendorID, payment_type

ORDER BY VendorID, payment_type;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# con = duckdb.connect()
# query = """
# SELECT
#     VendorID,
#     payment_type,
#     COUNT(*) AS trips,

#     ROUND(MIN(trip_distance), 2) AS min_distance,

#     ROUND(
#         QUANTILE_CONT(trip_distance, 0.25),
#         2
#     ) AS p25_distance,

#     ROUND(
#         QUANTILE_CONT(trip_distance, 0.50),
#         2
#     ) AS median_distance,

#     ROUND(
#         QUANTILE_CONT(trip_distance, 0.75),
#         2
#     ) AS p75_distance,

#     ROUND(
#         QUANTILE_CONT(trip_distance, 0.99),
#         2
#     ) AS p99_distance,

#     ROUND(MAX(trip_distance), 2) AS max_distance

# FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')

# GROUP BY VendorID, payment_type

# ORDER BY VendorID, payment_type;
# """

# result = con.execute(query).fetchdf()

# print(result.to_string(index=False))

# con.close()

