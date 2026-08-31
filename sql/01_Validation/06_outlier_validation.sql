-- ============================================================
-- 06. Outlier Validation
-- ============================================================
-- Purpose:
-- Identify extreme but potentially valid observations in the
-- staging tables.
------------------

-- Outliers are NOT automatically considered data-quality errors.
-- They are flagged for REVIEW because extreme trips, distances,
-- and fares can have legitimate business explanations.
-------------------------------------------------------

-- Thresholds are based on the exploratory analysis performed
-- on the January 2026 datasets.
-- ============================================================

WITH outlier_checks AS (

-- --------------------------------------------------------
-- Yellow Taxi
-- --------------------------------------------------------

SELECT
    'yellow_trips' AS dataset,
    'trip_distance_over_100_miles' AS check_name,
    COUNT(*) FILTER (
        WHERE trip_distance > 100
    ) AS outlier_count
FROM staging.yellow_trips

UNION ALL

SELECT
    'yellow_trips',
    'trip_duration_over_3_hours',
    COUNT(*) FILTER (
        WHERE tpep_dropoff_datetime - tpep_pickup_datetime
              > INTERVAL '3 hours'
    )
FROM staging.yellow_trips

UNION ALL

SELECT
    'yellow_trips',
    'total_amount_over_500',
    COUNT(*) FILTER (
        WHERE total_amount > 500
    )
FROM staging.yellow_trips


-- --------------------------------------------------------
-- Green Taxi
-- --------------------------------------------------------

UNION ALL

SELECT
    'green_trips',
    'trip_distance_over_100_miles',
    COUNT(*) FILTER (
        WHERE trip_distance > 100
    )
FROM staging.green_trips

UNION ALL

SELECT
    'green_trips',
    'trip_duration_over_3_hours',
    COUNT(*) FILTER (
        WHERE lpep_dropoff_datetime - lpep_pickup_datetime
              > INTERVAL '3 hours'
    )
FROM staging.green_trips

UNION ALL

SELECT
    'green_trips',
    'total_amount_over_500',
    COUNT(*) FILTER (
        WHERE total_amount > 500
    )
FROM staging.green_trips


-- --------------------------------------------------------
-- FHV
-- --------------------------------------------------------

UNION ALL

SELECT
    'fhv_trips',
    'trip_duration_over_3_hours',
    COUNT(*) FILTER (
        WHERE dropoff_datetime - pickup_datetime
              > INTERVAL '3 hours'
    )
FROM staging.fhv_trips


-- --------------------------------------------------------
-- FHVHV
-- --------------------------------------------------------

UNION ALL

SELECT
    'fhvhv_trips',
    'trip_miles_over_100',
    COUNT(*) FILTER (
        WHERE trip_miles > 100
    )
FROM staging.fhvhv_trips

UNION ALL

SELECT
    'fhvhv_trips',
    'trip_time_over_3_hours',
    COUNT(*) FILTER (
        WHERE trip_time > 10800
    )
FROM staging.fhvhv_trips

UNION ALL

SELECT
    'fhvhv_trips',
    'base_passenger_fare_over_500',
    COUNT(*) FILTER (
        WHERE base_passenger_fare > 500
    )
FROM staging.fhvhv_trips

)

---

-- Final Validation Result

---

SELECT
dataset,
check_name,
outlier_count,
CASE
WHEN outlier_count = 0
THEN 'PASS'
ELSE 'REVIEW'
END AS validation_status
FROM outlier_checks
ORDER BY
dataset,
check_name;
