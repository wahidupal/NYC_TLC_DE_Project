-- ============================================================
-- 07. Domain Validation
-- ============================================================
-- Purpose:
-- Validate categorical and identifier values against their
-- expected domains after ingestion.
------------------------------------

-- NULL values are handled separately in 03_null_validation.sql.
-- This check focuses on non-NULL values that fall outside the
-- expected domain.
-------------------

-- Domain violations are treated as data-quality failures because
-- they indicate values that do not conform to the expected
-- structure of the source dataset.
-- ============================================================

WITH domain_checks AS (

-- --------------------------------------------------------
-- Yellow Taxi
-- --------------------------------------------------------

SELECT
    'yellow_trips' AS dataset,
    'invalid_vendorid' AS check_name,
    COUNT(*) FILTER (
        WHERE vendorid IS NOT NULL
          AND vendorid NOT IN (1, 2, 6, 7)
    ) AS violation_count
FROM staging.yellow_trips

UNION ALL

SELECT
    'yellow_trips',
    'invalid_ratecodeid',
    COUNT(*) FILTER (
        WHERE ratecodeid IS NOT NULL
          AND ratecodeid NOT IN (1, 2, 3, 4, 5, 6, 99)
    )
FROM staging.yellow_trips

UNION ALL

SELECT
    'yellow_trips',
    'invalid_payment_type',
    COUNT(*) FILTER (
        WHERE payment_type IS NOT NULL
          AND payment_type NOT IN (0, 1, 2, 3, 4, 5, 6)
    )
FROM staging.yellow_trips

UNION ALL

SELECT
    'yellow_trips',
    'invalid_store_and_fwd_flag',
    COUNT(*) FILTER (
        WHERE store_and_fwd_flag IS NOT NULL
          AND store_and_fwd_flag NOT IN ('Y', 'N')
    )
FROM staging.yellow_trips

UNION ALL

SELECT
    'yellow_trips',
    'invalid_passenger_count',
    COUNT(*) FILTER (
        WHERE passenger_count IS NOT NULL
          AND passenger_count < 0
    )
FROM staging.yellow_trips


-- --------------------------------------------------------
-- Green Taxi
-- --------------------------------------------------------

UNION ALL

SELECT
    'green_trips',
    'invalid_vendorid',
    COUNT(*) FILTER (
        WHERE vendorid IS NOT NULL
          AND vendorid NOT IN (1, 2, 6, 7)
    )
FROM staging.green_trips

UNION ALL

SELECT
    'green_trips',
    'invalid_ratecodeid',
    COUNT(*) FILTER (
        WHERE ratecodeid IS NOT NULL
          AND ratecodeid NOT IN (1, 2, 3, 4, 5, 6, 99)
    )
FROM staging.green_trips

UNION ALL

SELECT
    'green_trips',
    'invalid_payment_type',
    COUNT(*) FILTER (
        WHERE payment_type IS NOT NULL
          AND payment_type NOT IN (0, 1, 2, 3, 4, 5, 6)
    )
FROM staging.green_trips

UNION ALL

SELECT
    'green_trips',
    'invalid_trip_type',
    COUNT(*) FILTER (
        WHERE trip_type IS NOT NULL
          AND trip_type NOT IN (1, 2)
    )
FROM staging.green_trips

UNION ALL

SELECT
    'green_trips',
    'invalid_store_and_fwd_flag',
    COUNT(*) FILTER (
        WHERE store_and_fwd_flag IS NOT NULL
          AND store_and_fwd_flag NOT IN ('Y', 'N')
    )
FROM staging.green_trips

UNION ALL

SELECT
    'green_trips',
    'invalid_passenger_count',
    COUNT(*) FILTER (
        WHERE passenger_count IS NOT NULL
          AND passenger_count < 0
    )
FROM staging.green_trips


-- --------------------------------------------------------
-- FHV
-- --------------------------------------------------------

UNION ALL

SELECT
    'fhv_trips',
    'invalid_location_id',
    COUNT(*) FILTER (
        WHERE (pulocationid IS NOT NULL AND pulocationid < 1)
           OR (dolocationid IS NOT NULL AND dolocationid < 1)
    )
FROM staging.fhv_trips


-- --------------------------------------------------------
-- FHVHV
-- --------------------------------------------------------

UNION ALL

SELECT
    'fhvhv_trips',
    'invalid_hvfhs_license_num',
    COUNT(*) FILTER (
        WHERE hvfhs_license_num IS NOT NULL
          AND hvfhs_license_num NOT IN ('HV0003', 'HV0005')
    )
FROM staging.fhvhv_trips

UNION ALL

SELECT
    'fhvhv_trips',
    'invalid_shared_request_flag',
    COUNT(*) FILTER (
        WHERE shared_request_flag IS NOT NULL
          AND shared_request_flag NOT IN ('Y', 'N')
    )
FROM staging.fhvhv_trips

UNION ALL

SELECT
    'fhvhv_trips',
    'invalid_shared_match_flag',
    COUNT(*) FILTER (
        WHERE shared_match_flag IS NOT NULL
          AND shared_match_flag NOT IN ('Y', 'N')
    )
FROM staging.fhvhv_trips

UNION ALL

SELECT
    'fhvhv_trips',
    'invalid_access_a_ride_flag',
    COUNT(*) FILTER (
        WHERE access_a_ride_flag IS NOT NULL
          AND access_a_ride_flag NOT IN ('Y', 'N')
    )
FROM staging.fhvhv_trips

UNION ALL

SELECT
    'fhvhv_trips',
    'invalid_wav_request_flag',
    COUNT(*) FILTER (
        WHERE wav_request_flag IS NOT NULL
          AND wav_request_flag NOT IN ('Y', 'N')
    )
FROM staging.fhvhv_trips

UNION ALL

SELECT
    'fhvhv_trips',
    'invalid_wav_match_flag',
    COUNT(*) FILTER (
        WHERE wav_match_flag IS NOT NULL
          AND wav_match_flag NOT IN ('Y', 'N')
    )
FROM staging.fhvhv_trips
)

---

-- Final Validation Result

---

SELECT
dataset,
check_name,
violation_count,
CASE
	WHEN violation_count = 0
	THEN 'PASS'
	ELSE 'FAIL'
	END AS validation_status
FROM domain_checks
ORDER BY
dataset,
check_name;
