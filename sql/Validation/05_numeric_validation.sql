-- ============================================================
-- 05. Numeric Validation
-- ============================================================
-- Purpose:
-- Validate objectively invalid numeric values in the staging
-- tables after ingestion.
--
-- Hard validation focuses on values that violate basic
-- numerical expectations, such as negative distance or time.
--
-- Large positive values are not automatically considered
-- invalid. Extreme values are treated as outliers and were
-- investigated separately during EDA.
--
-- Financial fields that may contain legitimate negative
-- adjustments are reported as REVIEW rather than FAIL.
-- These records are preserved in the staging layer.
-- ============================================================


WITH numeric_checks AS (

    -- --------------------------------------------------------
    -- Yellow Taxi
    -- --------------------------------------------------------

    SELECT
        'yellow_trips' AS dataset,
        'negative_trip_distance' AS check_name,
        COUNT(*) FILTER (
            WHERE trip_distance < 0
        ) AS violation_count,
        'HARD' AS check_type
    FROM staging.yellow_trips

    UNION ALL

    SELECT
        'yellow_trips',
        'negative_tolls_amount',
        COUNT(*) FILTER (
            WHERE tolls_amount < 0
        ),
        'REVIEW'
    FROM staging.yellow_trips

    UNION ALL

    SELECT
        'yellow_trips',
        'negative_total_amount',
        COUNT(*) FILTER (
            WHERE total_amount < 0
        ),
        'REVIEW'
    FROM staging.yellow_trips


    -- --------------------------------------------------------
    -- Green Taxi
    -- --------------------------------------------------------

    UNION ALL

    SELECT
        'green_trips',
        'negative_trip_distance',
        COUNT(*) FILTER (
            WHERE trip_distance < 0
        ),
        'HARD'
    FROM staging.green_trips

    UNION ALL

    SELECT
        'green_trips',
        'negative_tolls_amount',
        COUNT(*) FILTER (
            WHERE tolls_amount < 0
        ),
        'REVIEW'
    FROM staging.green_trips

    UNION ALL

    SELECT
        'green_trips',
        'negative_total_amount',
        COUNT(*) FILTER (
            WHERE total_amount < 0
        ),
        'REVIEW'
    FROM staging.green_trips


    -- --------------------------------------------------------
    -- FHV
    -- --------------------------------------------------------

    UNION ALL

    SELECT
        'fhv_trips',
        'negative_location_id',
        COUNT(*) FILTER (
            WHERE pulocationid < 0
               OR dolocationid < 0
        ),
        'HARD'
    FROM staging.fhv_trips


    -- --------------------------------------------------------
    -- FHVHV
    -- --------------------------------------------------------

    UNION ALL

    SELECT
        'fhvhv_trips',
        'negative_trip_miles',
        COUNT(*) FILTER (
            WHERE trip_miles < 0
        ),
        'HARD'
    FROM staging.fhvhv_trips

    UNION ALL

    SELECT
        'fhvhv_trips',
        'negative_trip_time',
        COUNT(*) FILTER (
            WHERE trip_time < 0
        ),
        'HARD'
    FROM staging.fhvhv_trips

    UNION ALL

    SELECT
        'fhvhv_trips',
        'negative_driver_pay',
        COUNT(*) FILTER (
            WHERE driver_pay < 0
        ),
        'REVIEW'
    FROM staging.fhvhv_trips

    UNION ALL

    SELECT
        'fhvhv_trips',
        'negative_base_passenger_fare',
        COUNT(*) FILTER (
            WHERE base_passenger_fare < 0
        ),
        'REVIEW'
    FROM staging.fhvhv_trips
)


-- ------------------------------------------------------------
-- Final Validation Result
-- ------------------------------------------------------------

SELECT
    dataset,
    check_name,
    violation_count,
    CASE
        WHEN violation_count = 0 THEN 'PASS'
        WHEN check_type = 'REVIEW' THEN 'REVIEW'
        ELSE 'FAIL'
    END AS validation_status
FROM numeric_checks
ORDER BY
    dataset,
    check_name;