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



