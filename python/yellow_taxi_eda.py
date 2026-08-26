# ============================================================
# NYC TLC Yellow Taxi Data - EDA Template
# ============================================================
# Dataset:
# yellow_tripdata_2026-01.parquet
#
# Purpose:
# Reusable SQL/EDA reference for future projects.
#
# Database:
# DuckDB
#
# ============================================================

# ============================================================
# 00. SETUP / DATASET PATH
# ============================================================

DATASET = '../data/raw/yellow_tripdata_2026-01.parquet'

# ============================================================
# 01. DATASET OVERVIEW
# ============================================================

# Total number of rows
"""
SELECT COUNT(*) AS total_trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""


# Dataset schema
"""
DESCRIBE
SELECT *
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""


# Statistical summary of all columns
"""
SUMMARIZE
SELECT *
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""


# ============================================================
# 02. NULL ANALYSIS
# ============================================================

# Count NULLs in a specific column
"""
SELECT COUNT(*) AS null_count
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE column_name IS NULL;
"""


# Count NULLs across multiple columns
"""
SELECT
    COUNT(*) FILTER (WHERE VendorID IS NULL) AS VendorID_nulls,
    COUNT(*) FILTER (WHERE trip_distance IS NULL) AS trip_distance_nulls,
    COUNT(*) FILTER (WHERE fare_amount IS NULL) AS fare_amount_nulls,
    COUNT(*) FILTER (WHERE total_amount IS NULL) AS total_amount_nulls
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""


# Count rows where multiple columns are NULL simultaneously
"""
SELECT COUNT(*) AS all_null
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE column_1 IS NULL
  AND column_2 IS NULL
  AND column_3 IS NULL;
"""


# Count rows where ANY of several columns is NULL
"""
SELECT COUNT(*) AS incomplete_trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE column_1 IS NULL
   OR column_2 IS NULL
   OR column_3 IS NULL;
"""


# NULL percentage
"""
SELECT
    COUNT(*) AS total_trips,
    COUNT(*) FILTER (WHERE column_name IS NULL) AS null_count,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE column_name IS NULL) / COUNT(*),
        2
    ) AS null_percentage
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""


# ============================================================
# 03. TIMESTAMP QUALITY
# ============================================================

# Extract duration in minutes using EPOCH
"""
SELECT
    EXTRACT(
        EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)
    ) / 60 AS duration_minutes
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""


# Count zero-duration trips
"""
SELECT COUNT(*) AS zero_duration_trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE EXTRACT(
    EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)
) = 0;
"""


# Count negative-duration trips
"""
SELECT COUNT(*) AS negative_duration_trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE tpep_dropoff_datetime < tpep_pickup_datetime;
"""


# Basic duration statistics
"""
SELECT
    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)
            ) / 60
        ),
        2
    ) AS avg_duration_minutes,

    ROUND(
        QUANTILE_CONT(
            EXTRACT(
                EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)
            ) / 60,
            0.50
        ),
        2
    ) AS median_duration_minutes,

    ROUND(
        QUANTILE_CONT(
            EXTRACT(
                EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)
            ) / 60,
            0.99
        ),
        2
    ) AS p99_duration_minutes,

    ROUND(
        MAX(
            EXTRACT(
                EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)
            ) / 60
        ),
        2
    ) AS max_duration_minutes

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""


# ============================================================
# 04. NUMERIC QUALITY
# ============================================================

# Check negative values
"""
SELECT COUNT(*) AS negative_values
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE fare_amount < 0;
"""


# Check zero values
"""
SELECT COUNT(*) AS zero_values
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
WHERE trip_distance = 0;
"""


# Check basic numeric statistics
"""
SELECT
    ROUND(AVG(trip_distance), 2) AS avg_distance,
    ROUND(
        QUANTILE_CONT(trip_distance, 0.50),
        2
    ) AS median_distance,
    ROUND(
        QUANTILE_CONT(trip_distance, 0.99),
        2
    ) AS p99_distance,
    ROUND(MAX(trip_distance), 2) AS max_distance
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""


# ============================================================
# 05. OUTLIER ANALYSIS
# ============================================================

# Count observations above thresholds
"""
SELECT
    COUNT(*) FILTER (WHERE trip_distance > 20) AS over_20,
    COUNT(*) FILTER (WHERE trip_distance > 50) AS over_50,
    COUNT(*) FILTER (WHERE trip_distance > 100) AS over_100,
    COUNT(*) FILTER (WHERE trip_distance > 500) AS over_500,
    COUNT(*) FILTER (WHERE trip_distance > 1000) AS over_1000
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""


# Inspect extreme observations
"""
SELECT *
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
ORDER BY trip_distance DESC
LIMIT 20;
"""


# ============================================================
# 06. VENDOR ANALYSIS
# ============================================================

# Number of trips by vendor
"""
SELECT
    VendorID,
    COUNT(*) AS total_trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
GROUP BY VendorID
ORDER BY total_trips DESC;
"""


# Compare averages by vendor
"""
SELECT
    VendorID,
    COUNT(*) AS total_trips,
    ROUND(AVG(trip_distance), 2) AS avg_trip_distance,
    ROUND(AVG(fare_amount), 2) AS avg_fare_amount,
    ROUND(AVG(total_amount), 2) AS avg_total_amount
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
GROUP BY VendorID;
"""


# Compare medians by vendor
"""
SELECT
    VendorID,
    ROUND(QUANTILE_CONT(trip_distance, 0.50), 2) AS median_distance,
    ROUND(QUANTILE_CONT(fare_amount, 0.50), 2) AS median_fare,
    ROUND(QUANTILE_CONT(total_amount, 0.50), 2) AS median_total
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
GROUP BY VendorID;
"""


# ============================================================
# 07. DISTANCE BUCKETING
# ============================================================

# Basic CASE WHEN bucketing
"""
SELECT
    CASE
        WHEN trip_distance < 1 THEN 'below_1'
        WHEN trip_distance < 2 THEN 'between_1_2'
        WHEN trip_distance < 5 THEN 'between_2_5'
        WHEN trip_distance < 10 THEN 'between_5_10'
        WHEN trip_distance < 20 THEN 'between_10_20'
        WHEN trip_distance < 50 THEN 'between_20_50'
        ELSE '50+'
    END AS distance_bucket,
    COUNT(*) AS trips
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
GROUP BY distance_bucket
ORDER BY trips DESC;
"""


# Distance buckets + multiple metrics
"""
WITH bucketed AS (
    SELECT
        CASE
            WHEN trip_distance < 1 THEN 'below_1'
            WHEN trip_distance < 2 THEN 'between_1_2'
            WHEN trip_distance < 5 THEN 'between_2_5'
            WHEN trip_distance < 10 THEN 'between_5_10'
            WHEN trip_distance < 20 THEN 'between_10_20'
            WHEN trip_distance < 50 THEN 'between_20_50'
            ELSE '50+'
        END AS distance_bucket,

        trip_distance,
        fare_amount,
        total_amount,

        EXTRACT(
            EPOCH FROM (
                tpep_dropoff_datetime - tpep_pickup_datetime
            )
        ) / 60 AS duration_minutes

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
    ROUND(AVG(duration_minutes), 2) AS avg_duration,
    ROUND(
        QUANTILE_CONT(duration_minutes, 0.50),
        2
    ) AS median_duration,
    ROUND(AVG(fare_amount), 2) AS avg_fare,
    ROUND(AVG(total_amount), 2) AS avg_total

FROM bucketed

GROUP BY distance_bucket

ORDER BY
    CASE distance_bucket
        WHEN 'below_1' THEN 1
        WHEN 'between_1_2' THEN 2
        WHEN 'between_2_5' THEN 3
        WHEN 'between_5_10' THEN 4
        WHEN 'between_10_20' THEN 5
        WHEN 'between_20_50' THEN 6
        WHEN '50+' THEN 7
    END;
"""


# ============================================================
# 08. FINANCIAL RECONCILIATION
# ============================================================

# Check whether total_amount matches component charges
"""
SELECT COUNT(*) AS mismatched_trips

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')

WHERE
    fare_amount
    + extra
    + mta_tax
    + tip_amount
    + tolls_amount
    + improvement_surcharge
    + COALESCE(congestion_surcharge, 0)
    + COALESCE(Airport_fee, 0)
    + COALESCE(cbd_congestion_fee, 0)
    != total_amount;
"""


# Calculate the difference
"""
SELECT
    total_amount
    - (
        fare_amount
        + extra
        + mta_tax
        + tip_amount
        + tolls_amount
        + improvement_surcharge
        + COALESCE(congestion_surcharge, 0)
        + COALESCE(Airport_fee, 0)
        + COALESCE(cbd_congestion_fee, 0)
    ) AS difference

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""


# Distribution of reconciliation differences
"""
SELECT
    difference,
    COUNT(*) AS trips

FROM (
    SELECT
        ROUND(
            total_amount
            - (
                fare_amount
                + extra
                + mta_tax
                + tip_amount
                + tolls_amount
                + improvement_surcharge
                + COALESCE(congestion_surcharge, 0)
                + COALESCE(Airport_fee, 0)
                + COALESCE(cbd_congestion_fee, 0)
            ),
            2
        ) AS difference

    FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
) t

GROUP BY difference

ORDER BY difference;
"""


# Investigate reconciliation by payment type
"""
SELECT
    payment_type,
    COUNT(*) AS trips,
    ROUND(AVG(difference), 2) AS avg_difference

FROM (
    SELECT
        payment_type,

        total_amount
        - (
            fare_amount
            + extra
            + mta_tax
            + tip_amount
            + tolls_amount
            + improvement_surcharge
            + COALESCE(congestion_surcharge, 0)
            + COALESCE(Airport_fee, 0)
            + COALESCE(cbd_congestion_fee, 0)
        ) AS difference

    FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
) t

GROUP BY payment_type

ORDER BY payment_type;
"""


# Investigate reconciliation by vendor
"""
SELECT
    VendorID,
    COUNT(*) AS trips,
    ROUND(AVG(difference), 2) AS avg_difference

FROM (
    SELECT
        VendorID,

        total_amount
        - (
            fare_amount
            + extra
            + mta_tax
            + tip_amount
            + tolls_amount
            + improvement_surcharge
            + COALESCE(congestion_surcharge, 0)
            + COALESCE(Airport_fee, 0)
            + COALESCE(cbd_congestion_fee, 0)
        ) AS difference

    FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
) t

GROUP BY VendorID

ORDER BY VendorID;
"""


# ============================================================
# 09. FINAL FINDINGS
# ============================================================

# Record your conclusions here.
#
# Example:
#
# 1. Dataset contains X trips.
# 2. NULLs are concentrated in specific columns.
# 3. Timestamp data contains X zero-duration trips.
# 4. Negative-duration trips are rare/common.
# 5. Trip distance is heavily right-skewed.
# 6. Extreme distance/duration values require investigation.
# 7. Vendors have noticeably different data characteristics.
# 8. Distance buckets reveal differences in duration/fare.
# 9. total_amount does not always reconcile with component charges.
# 10. Some discrepancies appear systematic rather than random.
#
# IMPORTANT:
# Findings should be based on actual results, not assumptions.