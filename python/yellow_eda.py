import duckdb
# Total number of rows
con = duckdb.connect()
query = """
SELECT COUNT(*) AS total_trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""
# Count distinct values
result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT
    COUNT(DISTINCT VendorID) AS vendors,
    COUNT(DISTINCT payment_type) AS payment_types,
    COUNT(DISTINCT PULocationID) AS pickup_zones,
    COUNT(DISTINCT DOLocationID) AS dropoff_zones
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Schema / column information
con = duckdb.connect()
query = """
DESCRIBE
SELECT *
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# General descriptive statistics
con = duckdb.connect()
query = """
SUMMARIZE SELECT *

FROM read_parquet('../data/raw/fhvhv_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# NULL counting
con = duckdb.connect()
query = """
SELECT COUNT(*) AS null_count
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE VendorID IS NULL;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Several columns manually
con = duckdb.connect()
query = """
SELECT
    COUNT(*) FILTER (WHERE VendorID IS NULL) AS VendorID_nulls,
    COUNT(*) FILTER (WHERE trip_distance IS NULL) AS trip_distance_nulls,
    COUNT(*) FILTER (WHERE fare_amount IS NULL) AS fare_amount_nulls,
    COUNT(*) FILTER (WHERE total_amount IS NULL) AS total_amount_nulls
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

#Rows where several fields are NULL simultaneously 
con = duckdb.connect()
query = """
SELECT COUNT(*) AS incomplete_trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE
    VendorID IS NULL
    AND trip_distance IS NULL
    AND fare_amount IS NULL
    AND total_amount IS NULL;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Rows where ANY of several fields is NULL
con = duckdb.connect()
query = """
SELECT COUNT(*) AS incomplete_trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE
    VendorID IS NULL
    OR trip_distance IS NULL
    OR fare_amount IS NULL
    OR total_amount IS NULL;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# COUNT + FILTER
con = duckdb.connect()
query = """
SELECT
    COUNT(*) AS total_trips,
    COUNT(*) FILTER (WHERE trip_distance < 20) AS below_20,
    COUNT(*) FILTER (WHERE trip_distance >= 20 AND trip_distance < 50) AS between_20_50,
    COUNT(*) FILTER (WHERE trip_distance >= 50 AND trip_distance < 100) AS between_50_100,
    COUNT(*) FILTER (WHERE trip_distance >= 100) AS over_100
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Conditional percentage
con = duckdb.connect()
query = """
SELECT
    VendorID,
    COUNT(*) AS total_trips,

    COUNT(*) FILTER (
        WHERE store_and_fwd_flag IS NULL
    ) AS incomplete_trips,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE store_and_fwd_flag IS NULL
        ) / COUNT(*),
        2
    ) AS incomplete_pct

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
GROUP BY VendorID;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# AVG / MEAN / Rounded
con = duckdb.connect()
query = """
SELECT
    AVG(trip_distance) AS avg_trip_distance,
    AVG(fare_amount) AS avg_fare_amount,
    AVG(total_amount) AS avg_total_amount
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');

SELECT
    ROUND(AVG(trip_distance), 2) AS avg_trip_distance,
    ROUND(AVG(fare_amount), 2) AS avg_fare_amount,
    ROUND(AVG(total_amount), 2) AS avg_total_amount
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Mean / Median / Percentile
con = duckdb.connect()
query = """
SELECT
    ROUND(QUANTILE_CONT(trip_distance, 0.25), 2) AS p25,
    ROUND(QUANTILE_CONT(trip_distance, 0.50), 2) AS median,
    ROUND(QUANTILE_CONT(trip_distance, 0.75), 2) AS p75,
    ROUND(QUANTILE_CONT(trip_distance, 0.99), 2) AS p99
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Timestamp subtraction / EXTRACT EPOCH (Its used for turning timestamp in sec/mins/hours)
con = duckdb.connect()
query = """
SELECT
    tpep_dropoff_datetime - tpep_pickup_datetime AS trip_duration, 
    EXTRACT(
    EPOCH FROM (
        tpep_dropoff_datetime - tpep_pickup_datetime
    )
) AS duration_secs,

EXTRACT(
    EPOCH FROM (
        tpep_dropoff_datetime - tpep_pickup_datetime
    )
) / 60 AS duration_mins,

EXTRACT(
    EPOCH FROM (
        tpep_dropoff_datetime - tpep_pickup_datetime
    )
) / 3600 AS duration_hours
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
LIMIT 10;


"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Zero Duration / Negative duration / Positive duration
con = duckdb.connect()
query = """
SELECT COUNT(*) AS zero_duration_trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE
    EXTRACT(
        EPOCH FROM (
            tpep_dropoff_datetime - tpep_pickup_datetime
        )
    ) = 0;

SELECT COUNT(*) AS negative_duration_trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE tpep_dropoff_datetime < tpep_pickup_datetime;  

SELECT COUNT(*) AS positive_duration_trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE tpep_dropoff_datetime > tpep_pickup_datetime;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Investigate the actual bad records
con = duckdb.connect()
query = """
SELECT *
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE tpep_dropoff_datetime < tpep_pickup_datetime;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Duration statistics
con = duckdb.connect()
query = """
SELECT
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

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Outlier thresholds
con = duckdb.connect()
query = """
SELECT
    COUNT(*) AS total_trips,

    COUNT(*) FILTER (
        WHERE trip_distance > 20
    ) AS over_20,

    COUNT(*) FILTER (
        WHERE trip_distance > 50
    ) AS over_50,

    COUNT(*) FILTER (
        WHERE trip_distance > 100
    ) AS over_100,

    COUNT(*) FILTER (
        WHERE trip_distance > 500
    ) AS over_500,

    COUNT(*) FILTER (
        WHERE trip_distance > 1000
    ) AS over_1k

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

# CASE WHEN bucketing
con.close()

con = duckdb.connect()
query = """
SELECT 
    CASE
        WHEN trip_distance < 20 THEN 'below_20'
        WHEN trip_distance < 50 THEN 'between_20_50'
        WHEN trip_distance < 100 THEN 'between_50_100'
        WHEN trip_distance < 500 THEN 'between_100_500'
        WHEN trip_distance < 1000 THEN 'between_500_1000'
        WHEN trip_distance < 10000 THEN 'between_1k_10k'
        ELSE '10k+'
    END AS distance_bucket

FROM read_parquet('../data/raw/fhvhv_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# CASE + GROUP BY using a subquery
con = duckdb.connect()
query = """
SELECT
    distance_bucket,
    COUNT(*) AS trips
FROM (
    SELECT
        CASE
            WHEN trip_distance < 20 THEN 'below_20'
            WHEN trip_distance < 50 THEN 'between_20_50'
            WHEN trip_distance < 100 THEN 'between_50_100'
            WHEN trip_distance < 500 THEN 'between_100_500'
            WHEN trip_distance < 1000 THEN 'between_500_1000'
            WHEN trip_distance < 10000 THEN 'between_1k_10k'
            ELSE '10k+'
        END AS distance_bucket
    FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
) t
GROUP BY distance_bucket;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# CASE + CTE
con = duckdb.connect()
query = """
WITH bucketed AS (
    SELECT
        CASE
            WHEN trip_distance < 20 THEN 'below_20'
            WHEN trip_distance < 50 THEN 'between_20_50'
            WHEN trip_distance < 100 THEN 'between_50_100'
            WHEN trip_distance < 500 THEN 'between_100_500'
            WHEN trip_distance < 1000 THEN 'between_500_1000'
            WHEN trip_distance < 10000 THEN 'between_1k_10k'
            ELSE '10k+'
        END AS distance_bucket,

        trip_distance,
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        fare_amount,
        total_amount

    FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
)

SELECT
    distance_bucket,
    COUNT(*) AS trip_count,

    ROUND(AVG(trip_distance), 2) AS avg_distance,

    ROUND(
        QUANTILE_CONT(trip_distance, 0.50),
        2
    ) AS median_distance,

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

    ROUND(AVG(fare_amount), 2) AS avg_fare,
    ROUND(AVG(total_amount), 2) AS avg_total

FROM bucketed

GROUP BY distance_bucket;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# GROUP BY vendor
con = duckdb.connect()
query = """
SELECT
    VendorID,
    COUNT(*) AS trips,
    ROUND(AVG(trip_distance), 2) AS avg_distance,
    ROUND(AVG(fare_amount), 2) AS avg_fare,
    ROUND(AVG(total_amount), 2) AS avg_total
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
GROUP BY VendorID
ORDER BY trips DESC;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Vendor + conditional counts
con = duckdb.connect()
query = """
SELECT
    VendorID,

    COUNT(*) AS total_trips,

    COUNT(*) FILTER (
        WHERE trip_distance = 0
    ) AS zero_distance_trips,

    COUNT(*) FILTER (
        WHERE trip_distance > 100
    ) AS over_100_miles,

    COUNT(*) FILTER (
        WHERE tpep_dropoff_datetime = tpep_pickup_datetime
    ) AS zero_duration_trips

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')

GROUP BY VendorID;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Inspect anomalies by vendor
con = duckdb.connect()
query = """
SELECT
    VendorID,
    payment_type,
    trip_distance,
    fare_amount,
    total_amount,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    PULocationID,
    DOLocationID

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')

WHERE
    tpep_dropoff_datetime = tpep_pickup_datetime

ORDER BY trip_distance DESC;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Financial reconciliation
con = duckdb.connect()
query = """
SELECT COUNT(*) AS mismatched_trips

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')

WHERE
    COALESCE(fare_amount, 0)
    + COALESCE(extra, 0)
    + COALESCE(mta_tax, 0)
    + COALESCE(tip_amount, 0)
    + COALESCE(tolls_amount, 0)
    + COALESCE(improvement_surcharge, 0)
    + COALESCE(congestion_surcharge, 0)
    + COALESCE(Airport_fee, 0)
    + COALESCE(cbd_congestion_fee, 0)
    != total_amount;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Calculate the actual difference
con = duckdb.connect()
query = """
SELECT
    total_amount
    - (
        COALESCE(fare_amount, 0)
        + COALESCE(extra, 0)
        + COALESCE(mta_tax, 0)
        + COALESCE(tip_amount, 0)
        + COALESCE(tolls_amount, 0)
        + COALESCE(improvement_surcharge, 0)
        + COALESCE(congestion_surcharge, 0)
        + COALESCE(Airport_fee, 0)
        + COALESCE(cbd_congestion_fee, 0)
    ) AS difference

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')

LIMIT 20;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Difference statistics
con = duckdb.connect()
query = """
WITH financials AS (
    SELECT
        total_amount
        - (
            COALESCE(fare_amount, 0)
            + COALESCE(extra, 0)
            + COALESCE(mta_tax, 0)
            + COALESCE(tip_amount, 0)
            + COALESCE(tolls_amount, 0)
            + COALESCE(improvement_surcharge, 0)
            + COALESCE(congestion_surcharge, 0)
            + COALESCE(Airport_fee, 0)
            + COALESCE(cbd_congestion_fee, 0)
        ) AS difference

    FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
)

SELECT
    ROUND(AVG(difference), 2) AS avg_difference,
    ROUND(MEDIAN(difference), 2) AS median_difference,
    ROUND(QUANTILE_CONT(difference, 0.99), 2) AS p99_difference,
    ROUND(MAX(difference), 2) AS max_difference,
    ROUND(MIN(difference), 2) AS min_difference

FROM financials;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Investigate financial differences by payment type
con = duckdb.connect()
query = """
SELECT
    payment_type,

    COUNT(*) AS trips,

    ROUND(
        AVG(
            total_amount
            - (
                COALESCE(fare_amount, 0)
                + COALESCE(extra, 0)
                + COALESCE(mta_tax, 0)
                + COALESCE(tip_amount, 0)
                + COALESCE(tolls_amount, 0)
                + COALESCE(improvement_surcharge, 0)
                + COALESCE(congestion_surcharge, 0)
                + COALESCE(Airport_fee, 0)
                + COALESCE(cbd_congestion_fee, 0)
            )
        ),
        2
    ) AS avg_difference

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')

GROUP BY payment_type

ORDER BY payment_type;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Financial differences by surcharge combination
con = duckdb.connect()
query = """
SELECT
    congestion_surcharge,
    Airport_fee,
    cbd_congestion_fee,

    ROUND(
        AVG(
            total_amount
            - (
                COALESCE(fare_amount, 0)
                + COALESCE(extra, 0)
                + COALESCE(mta_tax, 0)
                + COALESCE(tip_amount, 0)
                + COALESCE(tolls_amount, 0)
                + COALESCE(improvement_surcharge, 0)
                + COALESCE(congestion_surcharge, 0)
                + COALESCE(Airport_fee, 0)
                + COALESCE(cbd_congestion_fee, 0)
            )
        ),
        2
    ) AS avg_difference,

    COUNT(*) AS trips

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')

GROUP BY
    congestion_surcharge,
    Airport_fee,
    cbd_congestion_fee

ORDER BY trips DESC;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# Find the actual largest financial discrepancies
con = duckdb.connect()
query = """
SELECT
    payment_type,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    congestion_surcharge,
    Airport_fee,
    cbd_congestion_fee,
    total_amount,

    total_amount
    - (
        COALESCE(fare_amount, 0)
        + COALESCE(extra, 0)
        + COALESCE(mta_tax, 0)
        + COALESCE(tip_amount, 0)
        + COALESCE(tolls_amount, 0)
        + COALESCE(improvement_surcharge, 0)
        + COALESCE(congestion_surcharge, 0)
        + COALESCE(Airport_fee, 0)
        + COALESCE(cbd_congestion_fee, 0)
    ) AS difference

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')

ORDER BY difference DESC

LIMIT 20;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# ORDER BY frequency
con = duckdb.connect()
query = """
SELECT
    VendorID,
    COUNT(*) AS trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
GROUP BY VendorID
ORDER BY trips DESC;

SELECT
    PULocationID,
    COUNT(*) AS trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
GROUP BY PULocationID
ORDER BY trips DESC
LIMIT 20;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# CTE pattern
con = duckdb.connect()
query = """
WITH cleaned AS (
    SELECT
        ...
    FROM read_parquet('../data/raw/file.parquet')
),

bucketed AS (
    SELECT
        CASE
            WHEN ...
            THEN ...
        END AS bucket,

        ...
    FROM cleaned
)

SELECT
    bucket,
    COUNT(*),
    AVG(...),
    MEDIAN(...)
FROM bucketed
GROUP BY bucket;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
DESCRIBE
SELECT *
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
DESCRIBE
SELECT *
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()