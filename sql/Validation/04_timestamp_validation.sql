-- ============================================================
-- 04. Timestamp Validation
-- ============================================================
-- Purpose:
-- Validate chronological consistency of timestamp columns
-- after ingestion into PostgreSQL staging tables.
--
-- A PASS means that the expected chronological relationship
-- is preserved without violations.
--
-- Unusual but valid durations are not automatically treated
-- as ingestion errors. Extreme-duration analysis is handled
-- separately during EDA / cleaning.
-- ============================================================


WITH timestamp_checks AS (

    -- --------------------------------------------------------
    -- Yellow Taxi
    -- pickup_datetime <= dropoff_datetime
    -- --------------------------------------------------------

    SELECT
        'yellow_trips' AS dataset,
        'pickup_before_dropoff' AS check_name,
        COUNT(*) FILTER (
            WHERE tpep_pickup_datetime > tpep_dropoff_datetime
        ) AS violation_count
    FROM staging.yellow_trips


    UNION ALL

    -- --------------------------------------------------------
    -- Green Taxi
    -- pickup_datetime <= dropoff_datetime
    -- --------------------------------------------------------

    SELECT
        'green_trips',
        'pickup_before_dropoff',
        COUNT(*) FILTER (
            WHERE lpep_pickup_datetime > lpep_dropoff_datetime
        )
    FROM staging.green_trips


    UNION ALL

    -- --------------------------------------------------------
    -- FHV
    -- pickup_datetime <= dropoff_datetime
    -- --------------------------------------------------------

    SELECT
        'fhv_trips',
        'pickup_before_dropoff',
        COUNT(*) FILTER (
            WHERE pickup_datetime > dropoff_datetime
        )
    FROM staging.fhv_trips


    UNION ALL

    -- --------------------------------------------------------
    -- FHVHV
    -- request_datetime <= on_scene_datetime
    -- --------------------------------------------------------

    SELECT
        'fhvhv_trips',
        'request_before_on_scene',
        COUNT(*) FILTER (
            WHERE request_datetime > on_scene_datetime
        )
    FROM staging.fhvhv_trips


    UNION ALL

    -- --------------------------------------------------------
    -- FHVHV
    -- on_scene_datetime <= pickup_datetime
    -- --------------------------------------------------------

    SELECT
        'fhvhv_trips',
        'on_scene_before_pickup',
        COUNT(*) FILTER (
            WHERE on_scene_datetime > pickup_datetime
        )
    FROM staging.fhvhv_trips


    UNION ALL

    -- --------------------------------------------------------
    -- FHVHV
    -- pickup_datetime <= dropoff_datetime
    -- --------------------------------------------------------

    SELECT
        'fhvhv_trips',
        'pickup_before_dropoff',
        COUNT(*) FILTER (
            WHERE pickup_datetime > dropoff_datetime
        )
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
        WHEN violation_count = 0
        THEN 'PASS'
        ELSE 'FAIL'
    END AS validation_status
FROM timestamp_checks
ORDER BY
    dataset,
    check_name;