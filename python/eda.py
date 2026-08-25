import duckdb

# con = duckdb.connect()
# query = """
# SELECT
#     VendorID,
#     payment_type,
#     trip_distance,
#     fare_amount,
#     total_amount,
#     tpep_pickup_datetime,
#     tpep_dropoff_datetime,
#     PULocationID,
#     DOLocationID
# FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
# WHERE VendorID = 7
#   AND tpep_dropoff_datetime = tpep_pickup_datetime
# LIMIT 20;
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
    trip_distance,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    congestion_surcharge,
    cbd_congestion_fee,
    total_amount,

    total_amount - (
        fare_amount
        + extra
        + mta_tax
        + tip_amount
        + tolls_amount
        + improvement_surcharge
        + COALESCE(congestion_surcharge, 0)
        + COALESCE(cbd_congestion_fee, 0)
    ) AS difference

FROM read_parquet('../data/raw/green_tripdata_2026-01.parquet')
WHERE VendorID = 6
ORDER BY difference DESC
LIMIT 20;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

