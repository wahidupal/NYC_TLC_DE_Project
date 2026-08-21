import duckdb

con = duckdb.connect()
query = """
SELECT
    COUNT(*) FILTER (WHERE trip_distance < 20) AS below_20,
    COUNT(*) FILTER (WHERE trip_distance >= 20 AND trip_distance < 50) AS between_20_50,
    COUNT(*) FILTER (WHERE trip_distance >= 50 AND trip_distance < 100) AS between_50_100,
    COUNT(*) FILTER (WHERE trip_distance >= 100 AND trip_distance < 500) AS between_100_500,
    COUNT(*) FILTER (WHERE trip_distance >= 500 AND trip_distance < 1000) AS between_500_1000,
    COUNT(*) FILTER (WHERE trip_distance >= 1000 AND trip_distance < 10000) AS between_1k_10k,
    COUNT(*) FILTER (WHERE trip_distance >= 10000) AS over_10k,
    AVG(
        ROUND(
            EXTRACT(EPOCH FROM (
                tpep_dropoff_datetime - tpep_pickup_datetime
            )) / 60,
            2
        )
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
    AVG (fare_amount) AS avg_fare_amount,
    AVG (total_amount) AS avg_total_amount


FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE VendorID = 2;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT 
Distance_Bucket,
COUNT (*) AS trip_count,
AVG(ROUND(EXTRACT(EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)) / 60,2)) AS avg_duration_minutes,
ROUND(QUANTILE_CONT(EXTRACT(EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)) / 60,0.50),2) AS median_duration_minutes,
AVG (fare_amount) AS avg_fare_amount,
AVG (total_amount) AS avg_total_amount
FROM (SELECT
    tpep_dropoff_datetime, tpep_pickup_datetime, fare_amount, total_amount,
    CASE 
        WHEN trip_distance < 20 THEN 'below_20'
        WHEN trip_distance < 50 THEN 'between_20_50'
        WHEN trip_distance < 100 THEN 'between_50_100'
        WHEN trip_distance < 500 THEN 'between_100_500'
        WHEN trip_distance < 1000 THEN 'between_500_1000'
        WHEN trip_distance < 10000 THEN 'between_1k_10k'
        ELSE '10k+'
    END AS Distance_Bucket
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE VendorID = 2) t

GROUP BY Distance_Bucket;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# con = duckdb.connect()
# query = """
# SELECT *
# FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
# LIMIT 1
# """

# result = con.execute(query).fetchdf()

# print(result.to_string(index=False))

# con.close()

