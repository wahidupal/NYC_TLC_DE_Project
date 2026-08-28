-- ============================================================
-- 03. NULL Validation
-- ============================================================
-- Purpose:
-- Validate NULL values in the staging tables after ingestion.
--
-- NULLs are not automatically considered data quality errors.
-- This check verifies that the NULL patterns observed during
-- EDA are preserved after ingestion.
--
-- Expected NULL counts were verified against the original
-- Parquet files.
-- ============================================================


WITH expected_nulls AS (

    -- --------------------------------------------------------
    -- Yellow Taxi
    -- --------------------------------------------------------

    SELECT
        'yellow_trips' AS table_name,
        'vendorid' AS column_name,
        0 AS expected_null_count

    UNION ALL
    SELECT 'yellow_trips', 'tpep_pickup_datetime', 0

    UNION ALL
    SELECT 'yellow_trips', 'tpep_dropoff_datetime', 0

    UNION ALL
    SELECT 'yellow_trips', 'passenger_count', 1088058

    UNION ALL
    SELECT 'yellow_trips', 'trip_distance', 0

    UNION ALL
    SELECT 'yellow_trips', 'ratecodeid', 1088058

    UNION ALL
    SELECT 'yellow_trips', 'store_and_fwd_flag', 1088058

    UNION ALL
    SELECT 'yellow_trips', 'pulocationid', 0

    UNION ALL
    SELECT 'yellow_trips', 'dolocationid', 0

    UNION ALL
    SELECT 'yellow_trips', 'payment_type', 0

    UNION ALL
    SELECT 'yellow_trips', 'fare_amount', 0

    UNION ALL
    SELECT 'yellow_trips', 'extra', 0

    UNION ALL
    SELECT 'yellow_trips', 'mta_tax', 0

    UNION ALL
    SELECT 'yellow_trips', 'tip_amount', 0

    UNION ALL
    SELECT 'yellow_trips', 'tolls_amount', 0

    UNION ALL
    SELECT 'yellow_trips', 'improvement_surcharge', 0

    UNION ALL
    SELECT 'yellow_trips', 'total_amount', 0

    UNION ALL
    SELECT 'yellow_trips', 'congestion_surcharge', 1088058

    UNION ALL
    SELECT 'yellow_trips', 'airport_fee', 1088058

    UNION ALL
    SELECT 'yellow_trips', 'cbd_congestion_fee', 0


    -- --------------------------------------------------------
    -- Green Taxi
    -- --------------------------------------------------------

    UNION ALL
    SELECT 'green_trips', 'store_and_fwd_flag', 5414

    UNION ALL
    SELECT 'green_trips', 'ratecodeid', 5414

    UNION ALL
    SELECT 'green_trips', 'passenger_count', 5414

    UNION ALL
    SELECT 'green_trips', 'payment_type', 5414

    UNION ALL
    SELECT 'green_trips', 'trip_type', 5415

    UNION ALL
    SELECT 'green_trips', 'ehail_fee', 40272


    -- --------------------------------------------------------
    -- FHV
    -- --------------------------------------------------------

    UNION ALL
    SELECT 'fhv_trips', 'pulocationid', 1646462

    UNION ALL
    SELECT 'fhv_trips', 'dolocationid', 216251

    UNION ALL
    SELECT 'fhv_trips', 'sr_flag', 1941722

    UNION ALL
    SELECT 'fhv_trips', 'affiliated_base_number', 141985


    -- --------------------------------------------------------
    -- FHVHV
    -- --------------------------------------------------------

    UNION ALL
    SELECT 'fhvhv_trips', 'originating_base_num', 5676843
),


actual_nulls AS (

    -- --------------------------------------------------------
    -- Yellow Taxi
    -- --------------------------------------------------------

    SELECT
        'yellow_trips' AS table_name,
        'vendorid' AS column_name,
        COUNT(*) FILTER (
            WHERE vendorid IS NULL
        ) AS actual_null_count
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'tpep_pickup_datetime',
        COUNT(*) FILTER (
            WHERE tpep_pickup_datetime IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'tpep_dropoff_datetime',
        COUNT(*) FILTER (
            WHERE tpep_dropoff_datetime IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'passenger_count',
        COUNT(*) FILTER (
            WHERE passenger_count IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'trip_distance',
        COUNT(*) FILTER (
            WHERE trip_distance IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'ratecodeid',
        COUNT(*) FILTER (
            WHERE ratecodeid IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'store_and_fwd_flag',
        COUNT(*) FILTER (
            WHERE store_and_fwd_flag IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'pulocationid',
        COUNT(*) FILTER (
            WHERE pulocationid IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'dolocationid',
        COUNT(*) FILTER (
            WHERE dolocationid IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'payment_type',
        COUNT(*) FILTER (
            WHERE payment_type IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'fare_amount',
        COUNT(*) FILTER (
            WHERE fare_amount IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'extra',
        COUNT(*) FILTER (
            WHERE extra IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'mta_tax',
        COUNT(*) FILTER (
            WHERE mta_tax IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'tip_amount',
        COUNT(*) FILTER (
            WHERE tip_amount IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'tolls_amount',
        COUNT(*) FILTER (
            WHERE tolls_amount IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'improvement_surcharge',
        COUNT(*) FILTER (
            WHERE improvement_surcharge IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'total_amount',
        COUNT(*) FILTER (
            WHERE total_amount IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'congestion_surcharge',
        COUNT(*) FILTER (
            WHERE congestion_surcharge IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'airport_fee',
        COUNT(*) FILTER (
            WHERE airport_fee IS NULL
        )
    FROM staging.yellow_trips

    UNION ALL
    SELECT
        'yellow_trips',
        'cbd_congestion_fee',
        COUNT(*) FILTER (
            WHERE cbd_congestion_fee IS NULL
        )
    FROM staging.yellow_trips


    -- --------------------------------------------------------
    -- Green Taxi
    -- --------------------------------------------------------

    UNION ALL
    SELECT
        'green_trips',
        'store_and_fwd_flag',
        COUNT(*) FILTER (
            WHERE store_and_fwd_flag IS NULL
        )
    FROM staging.green_trips

    UNION ALL
    SELECT
        'green_trips',
        'ratecodeid',
        COUNT(*) FILTER (
            WHERE ratecodeid IS NULL
        )
    FROM staging.green_trips

    UNION ALL
    SELECT
        'green_trips',
        'passenger_count',
        COUNT(*) FILTER (
            WHERE passenger_count IS NULL
        )
    FROM staging.green_trips

    UNION ALL
    SELECT
        'green_trips',
        'payment_type',
        COUNT(*) FILTER (
            WHERE payment_type IS NULL
        )
    FROM staging.green_trips

    UNION ALL
    SELECT
        'green_trips',
        'trip_type',
        COUNT(*) FILTER (
            WHERE trip_type IS NULL
        )
    FROM staging.green_trips

    UNION ALL
    SELECT
        'green_trips',
        'ehail_fee',
        COUNT(*) FILTER (
            WHERE ehail_fee IS NULL
        )
    FROM staging.green_trips


    -- --------------------------------------------------------
    -- FHV
    -- --------------------------------------------------------

    UNION ALL
    SELECT
        'fhv_trips',
        'pulocationid',
        COUNT(*) FILTER (
            WHERE pulocationid IS NULL
        )
    FROM staging.fhv_trips

    UNION ALL
    SELECT
        'fhv_trips',
        'dolocationid',
        COUNT(*) FILTER (
            WHERE dolocationid IS NULL
        )
    FROM staging.fhv_trips

    UNION ALL
    SELECT
        'fhv_trips',
        'sr_flag',
        COUNT(*) FILTER (
            WHERE sr_flag IS NULL
        )
    FROM staging.fhv_trips

    UNION ALL
    SELECT
        'fhv_trips',
        'affiliated_base_number',
        COUNT(*) FILTER (
            WHERE affiliated_base_number IS NULL
        )
    FROM staging.fhv_trips


    -- --------------------------------------------------------
    -- FHVHV
    -- --------------------------------------------------------

    UNION ALL
    SELECT
        'fhvhv_trips',
        'originating_base_num',
        COUNT(*) FILTER (
            WHERE originating_base_num IS NULL
        )
    FROM staging.fhvhv_trips
)


-- ------------------------------------------------------------
-- Final Validation Result
-- ------------------------------------------------------------

SELECT
    e.table_name,
    e.column_name,
    e.expected_null_count,
    a.actual_null_count,
    CASE
        WHEN e.expected_null_count = a.actual_null_count
        THEN 'PASS'
        ELSE 'FAIL'
    END AS validation_status
FROM expected_nulls e
JOIN actual_nulls a
    ON e.table_name = a.table_name
   AND e.column_name = a.column_name
ORDER BY
    e.table_name,
    e.column_name;