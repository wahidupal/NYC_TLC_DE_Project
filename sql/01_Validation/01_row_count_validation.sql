-- ============================================================
-- 01. Row Count Validation
-- ============================================================
-- Purpose:
-- Verify that all records from the source Parquet files
-- were successfully ingested into the PostgreSQL staging layer.
--
-- Expected row counts were established during the EDA phase.
-- ============================================================

SELECT
    'yellow' AS dataset,
    COUNT(*) AS actual_rows,
    3724889 AS expected_rows,
    COUNT(*) = 3724889 AS row_count_matches
FROM staging.yellow_trips

UNION ALL

SELECT
    'green',
    COUNT(*),
    40272,
    COUNT(*) = 40272
FROM staging.green_trips

UNION ALL

SELECT
    'fhv',
    COUNT(*),
    1941722,
    COUNT(*) = 1941722
FROM staging.fhv_trips

UNION ALL

SELECT
    'fhvhv',
    COUNT(*),
    20940373,
    COUNT(*) = 20940373
FROM staging.fhvhv_trips;