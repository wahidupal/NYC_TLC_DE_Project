import duckdb

# Check the timestamp sequence
con = duckdb.connect()
query = """
SELECT
    COUNT(*) FILTER (
        WHERE on_scene_datetime < request_datetime
    ) AS on_scene_before_request,

    COUNT(*) FILTER (
        WHERE pickup_datetime < on_scene_datetime
    ) AS pickup_before_on_scene,

    COUNT(*) FILTER (
        WHERE dropoff_datetime < pickup_datetime
    ) AS dropoff_before_pickup,

    COUNT(*) FILTER (
        WHERE pickup_datetime < request_datetime
    ) AS pickup_before_request

FROM read_parquet('../data/raw/fhvhv_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

#Check zero and negative durations
con = duckdb.connect()
query = """
SELECT
    COUNT(*) FILTER (
        WHERE on_scene_datetime = request_datetime
    ) AS zero_request_to_scene,

    COUNT(*) FILTER (
        WHERE pickup_datetime = on_scene_datetime
    ) AS zero_scene_to_pickup,

    COUNT(*) FILTER (
        WHERE dropoff_datetime = pickup_datetime
    ) AS zero_trip_duration,

    COUNT(*) FILTER (
        WHERE on_scene_datetime < request_datetime
    ) AS negative_request_to_scene,

    COUNT(*) FILTER (
        WHERE pickup_datetime < on_scene_datetime
    ) AS negative_scene_to_pickup,

    COUNT(*) FILTER (
        WHERE dropoff_datetime < pickup_datetime
    ) AS negative_trip_duration

FROM read_parquet('../data/raw/fhvhv_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

#Get the duration distribution
con = duckdb.connect()
query = """
SELECT
    ROUND(
        AVG(
            EXTRACT(EPOCH FROM (
                dropoff_datetime - pickup_datetime
            )) / 60
        ),
        2
    ) AS avg_trip_minutes,

    ROUND(
        QUANTILE_CONT(
            EXTRACT(EPOCH FROM (
                dropoff_datetime - pickup_datetime
            )) / 60,
            0.50
        ),
        2
    ) AS median_trip_minutes,

    ROUND(
        QUANTILE_CONT(
            EXTRACT(EPOCH FROM (
                dropoff_datetime - pickup_datetime
            )) / 60,
            0.99
        ),
        2
    ) AS p99_trip_minutes,

    ROUND(
        MAX(
            EXTRACT(EPOCH FROM (
                dropoff_datetime - pickup_datetime
            )) / 60
        ),
        2
    ) AS max_trip_minutes

FROM read_parquet('../data/raw/fhvhv_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Quickly check the extreme tail
con = duckdb.connect()
query = """
SELECT
    COUNT(*) AS total_trips,

    COUNT(*) FILTER (
        WHERE trip_time > 3600
    ) AS over_1h,

    COUNT(*) FILTER (
        WHERE trip_time > 7200
    ) AS over_2h,

    COUNT(*) FILTER (
        WHERE trip_time > 10800
    ) AS over_3h,

    COUNT(*) FILTER (
        WHERE trip_time > 86400
    ) AS over_1day

FROM read_parquet('../data/raw/fhvhv_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()


# Distance sanity check
con = duckdb.connect()
query = """
SELECT
    COUNT(*) AS total_trips,

    COUNT(*) FILTER (
        WHERE trip_miles = 0
    ) AS zero_distance_trips,

    COUNT(*) FILTER (
        WHERE trip_miles < 0
    ) AS negative_distance_trips,

    ROUND(AVG(trip_miles), 2) AS avg_trip_miles,

    ROUND(
        QUANTILE_CONT(trip_miles, 0.50),
        2
    ) AS median_trip_miles,

    ROUND(
        QUANTILE_CONT(trip_miles, 0.99),
        2
    ) AS p99_trip_miles,

    ROUND(MAX(trip_miles), 2) AS max_trip_miles

FROM read_parquet('../data/raw/fhvhv_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

#Distance sanity check
con = duckdb.connect()
query = """
WITH bucketed AS (
    SELECT
        CASE
            WHEN trip_miles < 1 THEN 'below_1'
            WHEN trip_miles < 2 THEN 'between_1_2'
            WHEN trip_miles < 5 THEN 'between_2_5'
            WHEN trip_miles < 10 THEN 'between_5_10'
            WHEN trip_miles < 20 THEN 'between_10_20'
            WHEN trip_miles < 50 THEN 'between_20_50'
            ELSE '50+'
        END AS distance_bucket,
        trip_miles,
        trip_time,
        base_passenger_fare,
        driver_pay
    FROM read_parquet('../data/raw/fhvhv_tripdata_2026-01.parquet')
)

SELECT
    distance_bucket,
    COUNT(*) AS trips,
    AVG(trip_miles) AS avg_miles,
    QUANTILE_CONT(trip_miles, 0.50) AS median_distance,
    AVG(trip_time) avg_trip_time,
    QUANTILE_CONT(trip_time, 0.50) AS median_trip_time,
    AVG(base_passenger_fare) AS avg_fare,
    AVG(driver_pay) AS avg_driver_pay

FROM bucketed
GROUP BY distance_bucket;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()



