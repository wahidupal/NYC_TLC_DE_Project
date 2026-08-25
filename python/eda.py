import duckdb

# con = duckdb.connect()
# query = """
# SELECT
#     DISTINCT VendorID,
# FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
# """

# result = con.execute(query).fetchdf()

# print(result.to_string(index=False))

# con.close()

con = duckdb.connect()
query = """
SELECT
    ROUND(
        QUANTILE_CONT(
            total_amount - (
                fare_amount
                + extra
                + mta_tax
                + tip_amount
                + tolls_amount
                + improvement_surcharge
                + COALESCE(congestion_surcharge, 0)
                + COALESCE(cbd_congestion_fee, 0)
            ),
            0.25
        ), 2
    ) AS p25_difference,

    ROUND(
        QUANTILE_CONT(
            total_amount - (
                fare_amount
                + extra
                + mta_tax
                + tip_amount
                + tolls_amount
                + improvement_surcharge
                + COALESCE(congestion_surcharge, 0)
                + COALESCE(cbd_congestion_fee, 0)
            ),
            0.50
        ), 2
    ) AS median_difference,

    ROUND(
        QUANTILE_CONT(
            total_amount - (
                fare_amount
                + extra
                + mta_tax
                + tip_amount
                + tolls_amount
                + improvement_surcharge
                + COALESCE(congestion_surcharge, 0)
                + COALESCE(cbd_congestion_fee, 0)
            ),
            0.75
        ), 2
    ) AS p75_difference,

    ROUND(
        QUANTILE_CONT(
            total_amount - (
                fare_amount
                + extra
                + mta_tax
                + tip_amount
                + tolls_amount
                + improvement_surcharge
                + COALESCE(congestion_surcharge, 0)
                + COALESCE(cbd_congestion_fee, 0)
            ),
            0.99
        ), 2
    ) AS p99_difference

FROM read_parquet('../data/raw/green_tripdata_2026-01.parquet')
WHERE VendorID = 6;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT
    VendorID,
    distance_bucket,
    COUNT(*) AS trips
FROM (
    SELECT
    VendorID,
    CASE
        WHEN trip_distance < 2 THEN 'below_2'
        WHEN trip_distance < 5 THEN 'between_2_5'
        WHEN trip_distance < 10 THEN 'between_5_10'
        WHEN trip_distance < 20 THEN 'between_10_20'
        ELSE '20+'
    END AS distance_bucket,
    trip_distance,
    fare_amount,
    total_amount
    FROM read_parquet('../data/raw/green_tripdata_2026-01.parquet')
) t
GROUP BY
    VendorID,
    distance_bucket
ORDER BY VendorID;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

