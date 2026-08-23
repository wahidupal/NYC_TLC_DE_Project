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
    COUNT(*) AS total_trips,
    COUNT(*) FILTER (
        WHERE congestion_surcharge IS NULL
    ) AS congestion_nulls,
    COUNT(*) FILTER (
        WHERE Airport_fee IS NULL
    ) AS airport_nulls,
    COUNT(*) FILTER (
        WHERE cbd_congestion_fee IS NULL
    ) AS cbd_nulls
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT 
payment_type,
COUNT (*) AS mismatched_trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE fare_amount + extra + mta_tax + tip_amount + tolls_amount + improvement_surcharge + congestion_surcharge + Airport_fee + cbd_congestion_fee != total_amount
GROUP BY payment_type
ORDER BY mismatched_trips DESC;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

