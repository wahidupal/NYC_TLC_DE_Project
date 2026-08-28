-- ============================================================
-- 02. Schema Validation
-- ============================================================
-- Purpose:
-- Verify the columns and data types of all PostgreSQL
-- staging tables after ingestion.
--
-- The query returns the schema of all four staging tables
-- in a single result set.
-- ============================================================

SELECT
    table_name,
    ordinal_position,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'staging'
  AND table_name IN (
      'yellow_trips',
      'green_trips',
      'fhv_trips',
      'fhvhv_trips'
  )
ORDER BY
    table_name,
    ordinal_position;