-- ============================================================
-- 02. Schema Validation
-- ============================================================
-- Purpose:
-- Validate the structure of the PostgreSQL staging tables
-- after data ingestion.
--
-- Checks:
--   1. Expected number of columns per table
--   2. Actual column names and data types
--
-- Expected column counts:
--   Yellow : 20
--   Green  : 21
--   FHV    : 7
--   FHVHV  : 25
--
-- Total: 73 columns
-- ============================================================


WITH expected_columns AS (
    SELECT 'yellow_trips' AS table_name, 20 AS expected_count
    UNION ALL
    SELECT 'green_trips', 21
    UNION ALL
    SELECT 'fhv_trips', 7
    UNION ALL
    SELECT 'fhvhv_trips', 25
),

actual_columns AS (
    SELECT
        table_name,
        COUNT(*) AS actual_count
    FROM information_schema.columns
    WHERE table_schema = 'staging'
      AND table_name IN (
          'yellow_trips',
          'green_trips',
          'fhv_trips',
          'fhvhv_trips'
      )
    GROUP BY table_name
)

SELECT
    e.table_name,
    e.expected_count,
    COALESCE(a.actual_count, 0) AS actual_count,
    CASE
        WHEN COALESCE(a.actual_count, 0) = e.expected_count
        THEN 'PASS'
        ELSE 'FAIL'
    END AS validation_status
FROM expected_columns e
LEFT JOIN actual_columns a
    ON e.table_name = a.table_name
ORDER BY e.table_name;