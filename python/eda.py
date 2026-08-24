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
SELECT COUNT(*) AS total_trips
FROM read_parquet('../data/raw/green_tripdata_2026-01.parquet')
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT
    VendorID,
    COUNT(*) AS total_trips,
    COUNT(*) FILTER (WHERE trip_distance IS NULL
                OR fare_amount IS NULL
                OR total_amount IS NULL
                OR lpep_pickup_datetime IS NULL
                OR lpep_dropoff_datetime IS NULL ) AS incomplete_trips
FROM read_parquet('../data/raw/green_tripdata_2026-01.parquet')
GROUP BY VendorID;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

